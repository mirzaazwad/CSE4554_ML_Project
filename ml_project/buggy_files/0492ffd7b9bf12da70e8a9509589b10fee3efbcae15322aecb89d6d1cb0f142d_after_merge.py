    def __call__(
        self, uid: str, data: Dict[str, Union[str, np.ndarray]]
    ) -> Dict[str, np.ndarray]:
        assert check_argument_types()

        if self.speech_name in data:
            # Nothing now: candidates:
            # - STFT
            # - Fbank
            # - CMVN
            # - Data augmentation
            pass

        for text_n in self.text_name:
            if text_n in data and self.tokenizer is not None:
                text = data[text_n]
                text = self.text_cleaner(text)
                tokens = self.tokenizer.text2tokens(text)
                text_ints = self.token_id_converter.tokens2ids(tokens)
                data[text_n] = np.array(text_ints, dtype=np.int64)
        assert check_return_type(data)
        return data