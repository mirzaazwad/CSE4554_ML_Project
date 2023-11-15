    def setData(self, index, value, role=Qt.EditRole, change_type=None):
        """Cell content change"""
        column = index.column()
        row = index.row()

        if change_type is not None:
            try:
                value = self.data(index, role=Qt.DisplayRole)
                val = from_qvariant(value, str)
                if change_type is bool:
                    val = bool_false_check(val)
                self.df.iloc[row, column - 1] = change_type(val)
            except ValueError:
                self.df.iloc[row, column - 1] = change_type('0')
        else:
            val = from_qvariant(value, str)
            current_value = self.get_value(row, column-1)
            if isinstance(current_value, (bool, np.bool_)):
                val = bool_false_check(val)
            supported_types = (bool, np.bool_) + REAL_NUMBER_TYPES
            if (isinstance(current_value, supported_types) or
                    is_text_string(current_value)):
                try:
                    self.df.iloc[row, column-1] = current_value.__class__(val)
                except (ValueError, OverflowError) as e:
                    QMessageBox.critical(self.dialog, "Error",
                                         str(type(e).__name__) + ": " + str(e))
                    return False
            else:
                QMessageBox.critical(self.dialog, "Error",
                                     "Editing dtype {0!s} not yet supported."
                                     .format(type(current_value).__name__))
                return False
        self.max_min_col_update()
        self.dataChanged.emit(index, index)
        return True