def _heat(image, sampled_diag, sigma):
    _sample_image(image, sampled_diag)  # modifies `heat` inplace
    image[:] = gaussian_filter(image, sigma, mode="reflect")