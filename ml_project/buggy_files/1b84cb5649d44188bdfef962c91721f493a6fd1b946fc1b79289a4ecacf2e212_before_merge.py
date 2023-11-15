    def forward_request(self, method, path, data, headers):
        data = data and json.loads(to_str(data))

        if re.match(PATH_REGEX_USER_REQUEST, path):
            search_match = re.search(PATH_REGEX_USER_REQUEST, path)
            api_id = search_match.group(1)
            stage = search_match.group(2)
            relative_path_w_query_params = '/%s' % search_match.group(3)

            relative_path, query_string_params = extract_query_string_params(path=relative_path_w_query_params)

            path_map = helpers.get_rest_api_paths(rest_api_id=api_id)
            try:
                extracted_path, resource = get_resource_for_path(path=relative_path, path_map=path_map)
            except Exception:
                return make_error('Unable to find path %s' % path, 404)

            integrations = resource.get('resourceMethods', {})
            integration = integrations.get(method, {})
            if not integration:
                integration = integrations.get('ANY', {})
            integration = integration.get('methodIntegration')
            if not integration:
                if method == 'OPTIONS' and 'Origin' in headers:
                    # default to returning CORS headers if this is an OPTIONS request
                    return get_cors_response(headers)
                return make_error('Unable to find integration for path %s' % path, 404)

            uri = integration.get('uri')
            if method == 'POST' and integration['type'] == 'AWS':
                if uri.endswith('kinesis:action/PutRecords'):
                    template = integration['requestTemplates'][APPLICATION_JSON]
                    new_request = aws_stack.render_velocity_template(template, data)

                    # forward records to target kinesis stream
                    headers = aws_stack.mock_aws_request_headers(service='kinesis')
                    headers['X-Amz-Target'] = kinesis_listener.ACTION_PUT_RECORDS
                    result = common.make_http_request(url=TEST_KINESIS_URL,
                        method='POST', data=new_request, headers=headers)
                    return result

                elif uri.startswith('arn:aws:apigateway:') and ':sqs:path' in uri:
                    template = integration['requestTemplates'][APPLICATION_JSON]
                    account_id, queue = uri.split('/')[-2:]
                    region_name = uri.split(':')[3]

                    new_request = aws_stack.render_velocity_template(template, data) + '&QueueName=%s' % queue
                    headers = aws_stack.mock_aws_request_headers(service='sqs', region_name=region_name)

                    url = urljoin(TEST_SQS_URL, '%s/%s?%s' % (account_id, queue, new_request))
                    result = common.make_http_request(url, method='GET', headers=headers)
                    return result

                else:
                    msg = 'API Gateway action uri "%s" not yet implemented' % uri
                    LOGGER.warning(msg)
                    return make_error(msg, 404)

            elif integration['type'] == 'AWS_PROXY':
                if uri.startswith('arn:aws:apigateway:') and ':lambda:path' in uri:
                    func_arn = uri.split(':lambda:path')[1].split('functions/')[1].split('/invocations')[0]
                    data_str = json.dumps(data) if isinstance(data, (dict, list)) else data
                    account_id = uri.split(':lambda:path')[1].split(':function:')[0].split(':')[-1]

                    source_ip = headers['X-Forwarded-For'].split(',')[-2]

                    # Sample request context:
                    # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html#api-gateway-create-api-as-simple-proxy-for-lambda-test
                    request_context = {
                        'path': relative_path,
                        'accountId': account_id,
                        'resourceId': resource.get('id'),
                        'stage': stage,
                        'identity': {
                            'accountId': account_id,
                            'sourceIp': source_ip,
                            'userAgent': headers['User-Agent'],
                        }
                    }

                    try:
                        path_params = extract_path_params(path=relative_path, extracted_path=extracted_path)
                    except Exception:
                        path_params = {}

                    result = lambda_api.process_apigateway_invocation(func_arn, relative_path, data_str,
                        headers, path_params=path_params, query_string_params=query_string_params,
                        method=method, resource_path=path, request_context=request_context)

                    if isinstance(result, FlaskResponse):
                        return flask_to_requests_response(result)

                    response = Response()
                    parsed_result = result if isinstance(result, dict) else json.loads(result)
                    parsed_result = common.json_safe(parsed_result)
                    response.status_code = int(parsed_result.get('statusCode', 200))
                    response.headers.update(parsed_result.get('headers', {}))
                    try:
                        if isinstance(parsed_result['body'], dict):
                            response._content = json.dumps(parsed_result['body'])
                        else:
                            response._content = parsed_result['body']
                    except Exception:
                        response._content = '{}'
                    return response
                else:
                    msg = 'API Gateway action uri "%s" not yet implemented' % uri
                    LOGGER.warning(msg)
                    return make_error(msg, 404)

            elif integration['type'] == 'HTTP':
                function = getattr(requests, method.lower())
                if isinstance(data, dict):
                    data = json.dumps(data)
                result = function(integration['uri'], data=data, headers=headers)
                return result

            else:
                msg = ('API Gateway integration type "%s" for method "%s" not yet implemented' %
                       (integration['type'], method))
                LOGGER.warning(msg)
                return make_error(msg, 404)

            return 200

        if re.match(PATH_REGEX_AUTHORIZERS, path):
            return handle_authorizers(method, path, data, headers)

        return True