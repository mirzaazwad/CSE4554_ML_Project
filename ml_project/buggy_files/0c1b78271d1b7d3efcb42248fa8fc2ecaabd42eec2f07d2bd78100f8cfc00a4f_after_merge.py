    def current_size(self, size: Union[None, float]) -> None:
        self._current_size = size
        if (
            self._update_properties
            and len(self.selected_data) > 0
            and self._mode != Mode.ADD
        ):
            for i in self.selected_data:
                self.size[i, :] = (self.size[i, :] > 0) * size
            self.refresh()
            self.events.size()
        self.status = format_float(self.current_size)