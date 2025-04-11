from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MultiLabelBinarizer

class StringToListTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, sep=';'):
        self.sep = sep

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(lambda val: val.split(self.sep) if isinstance(val, str) else []).values.reshape(-1, 1)

class MultiLabelBinarizerWrapper(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mlb = MultiLabelBinarizer()

    def fit(self, X, y=None):
        X_flat = [x[0] for x in X]
        return self.mlb.fit(X_flat)

    def transform(self, X):
        X_flat = [x[0] for x in X]
        return self.mlb.transform(X_flat)

class CategoricalPipeline(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.to_list = StringToListTransformer(sep=';')
        X_list = self.to_list.transform(X)
        self.binarizer = MultiLabelBinarizerWrapper()
        self.binarizer.fit(X_list)
        return self

    def transform(self, X):
        X_list = self.to_list.transform(X)
        return self.binarizer.transform(X_list)

class AssuntosPipeline(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.splitter = StringToListTransformer(sep=';')
        X_split = self.splitter.transform(X)
        self.binarizer = MultiLabelBinarizerWrapper()
        self.binarizer.fit(X_split)
        return self

    def transform(self, X):
        X_split = self.splitter.transform(X)
        return self.binarizer.transform(X_split)
