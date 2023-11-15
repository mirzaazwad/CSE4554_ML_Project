    def _sub_datelike(self, other):
        # subtract a datetime from myself, yielding a TimedeltaIndex
        from pandas import TimedeltaIndex
        other = Timestamp(other)
        if other is tslib.NaT:
            result = self._nat_new(box=False)
        # require tz compat
        elif not self._has_same_tz(other):
            raise TypeError("Timestamp subtraction must have the same "
                            "timezones or no timezones")
        else:
            i8 = self.asi8
            result = i8 - other.value
            result = self._maybe_mask_results(result, fill_value=tslib.iNaT)
        return TimedeltaIndex(result, name=self.name, copy=False)