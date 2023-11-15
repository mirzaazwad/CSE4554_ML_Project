    def help_settings(self):
        return [
            self.db_type,
            self.experiment_name,
            self.db_name,
            self.db_host,
            self.db_user,
            self.db_passwd,
            self.sqlite_file,
            self.allow_overwrite,
            self.want_table_prefix,
            self.table_prefix,
            self.save_cpa_properties,
            self.location_object,
            self.wants_properties_image_url_prepend,
            self.properties_image_url_prepend,
            self.properties_plate_type,
            self.properties_plate_metadata,
            self.properties_well_metadata,
            self.properties_export_all_image_defaults,
            self.image_groups[0].image_cols,
            self.image_groups[0].wants_automatic_image_name,
            self.image_groups[0].image_name,
            self.image_groups[0].image_channel_colors,
            self.properties_wants_groups,
            self.group_field_groups[0].group_name,
            self.group_field_groups[0].group_statement,
            self.properties_wants_filters,
            self.create_filters_for_plates,
            self.properties_class_table_name,
            self.directory,
            self.create_workspace_file,
            self.workspace_measurement_groups[0].measurement_display,
            self.workspace_measurement_groups[0].x_measurement_type,
            self.workspace_measurement_groups[0].x_object_name,
            self.workspace_measurement_groups[0].x_measurement_name,
            self.workspace_measurement_groups[0].y_measurement_type,
            self.workspace_measurement_groups[0].y_object_name,
            self.workspace_measurement_groups[0].y_measurement_name,
            self.wants_agg_mean,
            self.wants_agg_median,
            self.wants_agg_std_dev,
            self.wants_agg_mean_well,
            self.wants_agg_median_well,
            self.wants_agg_std_dev_well,
            self.objects_choice,
            self.objects_list,
            self.separate_object_tables,
            self.max_column_size,
            self.want_image_thumbnails,
            self.thumbnail_image_names,
            self.auto_scale_thumbnail_intensities,
        ]