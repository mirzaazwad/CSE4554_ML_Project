    def __init__(
        self,
        emission_coeff: Tensor,
        transition_coeff: Tensor,
        innovation_coeff: Tensor,
        noise_std: Tensor,
        residuals: Tensor,
        prior_mean: Tensor,
        prior_cov: Tensor,
        latent_dim: int,
        output_dim: int,
        seq_length: int,
    ) -> None:
        self.latent_dim = latent_dim
        self.output_dim = output_dim
        self.seq_length = seq_length

        # Split coefficients along time axis for easy access
        # emission_coef[t]: (batch_size, obs_dim, latent_dim)
        self.emission_coeff = emission_coeff.split(
            axis=1, num_outputs=self.seq_length, squeeze_axis=True
        )

        # innovation_coef[t]: (batch_size, latent_dim)
        self.innovation_coeff = innovation_coeff.split(
            axis=1, num_outputs=self.seq_length, squeeze_axis=False
        )

        # transition_coeff: (batch_size, latent_dim, latent_dim)
        self.transition_coeff = transition_coeff.split(
            axis=1, num_outputs=self.seq_length, squeeze_axis=True
        )

        # noise_std[t]: (batch_size, obs_dim)
        self.noise_std = noise_std.split(
            axis=1, num_outputs=self.seq_length, squeeze_axis=True
        )

        # residuals[t]: (batch_size, obs_dim)
        self.residuals = residuals.split(
            axis=1, num_outputs=self.seq_length, squeeze_axis=True
        )

        self.prior_mean = prior_mean
        self.prior_cov = prior_cov