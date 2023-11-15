    def export_savedmodel(self, *args, **kwargs):
        original = gorilla.get_original_attribute(tensorflow.estimator.Estimator,
                                                  'export_savedmodel')
        serialized = original(self, *args, **kwargs)
        try:
            log_model(tf_saved_model_dir=serialized.decode('utf-8'),
                      tf_meta_graph_tags=[tag_constants.SERVING],
                      tf_signature_def_key='predict',
                      artifact_path='model')
        except MlflowException as e:
            warnings.warn("Logging to MLflow failed: " + str(e))
        return serialized