# This is the first call to partial_fit:
# initialize various cumulative counters
n_features = X.shape[1]
n_classes = len(self.classes_)
self.theta_ = np.zeros((n_classes, n_features))
self.sigma_ = np.zeros((n_classes, n_features))

# Get the class count
self.class_count_ = np.zeros(n_classes, dtype=np.float64)

# Initialise the class prior
# Take into account the priors
if self.priors is not None:
    # Convert to array
    priors = np.asarray(self.priors)
    # Check that the provide prior match the number of classes
    if len(priors) != n_classes:
        raise ValueError('Number of priors must match number of'
                            ' classes.')
    # Check that the sum is 1
    if not np.isclose(priors.sum(), 1.0):
        raise ValueError('The sum of the priors should be 1.')
    # Check that the prior are non-negative
    if (priors < 0).any():
        raise ValueError('Priors must be non-negative.')
    self.class_prior_ = priors
#
else:
    # Initialize the priors to zeros for each class
    self.class_prior_ = np.zeros(len(self.classes_),
                                    dtype=np.float64)
