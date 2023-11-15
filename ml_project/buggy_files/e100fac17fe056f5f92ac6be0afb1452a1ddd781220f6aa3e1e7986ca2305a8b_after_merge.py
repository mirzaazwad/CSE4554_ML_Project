    def to_onnx(self, file_path: str, input_sample: Optional[Tensor] = None, **kwargs):
        """Saves the model in ONNX format

        Args:
            file_path: The path of the file the model should be saved to.
            input_sample: A sample of an input tensor for tracing.
            **kwargs: Will be passed to torch.onnx.export function.

        Example:
            >>> class SimpleModel(LightningModule):
            ...     def __init__(self):
            ...         super().__init__()
            ...         self.l1 = torch.nn.Linear(in_features=64, out_features=4)
            ...
            ...     def forward(self, x):
            ...         return torch.relu(self.l1(x.view(x.size(0), -1)))

            >>> with tempfile.NamedTemporaryFile(suffix='.onnx', delete=False) as tmpfile:
            ...     model = SimpleModel()
            ...     input_sample = torch.randn((1, 64))
            ...     model.to_onnx(tmpfile.name, input_sample, export_params=True)
            ...     os.path.isfile(tmpfile.name)
            True
        """

        if isinstance(input_sample, Tensor):
            input_data = input_sample
        elif self.example_input_array is not None:
            input_data = self.example_input_array
        else:
            if input_sample is not None:
                raise ValueError(f'Received `input_sample` of type {type(input_sample)}. Expected type is `Tensor`')
            else:
                raise ValueError('Could not export to ONNX since neither `input_sample` nor'
                                 ' `model.example_input_array` attribute is set.')
        input_data = input_data.to(self.device)
        if 'example_outputs' not in kwargs:
            self.eval()
            with torch.no_grad():
                kwargs['example_outputs'] = self(input_data)

        torch.onnx.export(self, input_data, file_path, **kwargs)