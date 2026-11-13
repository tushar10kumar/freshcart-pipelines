import pandas as pd
from sklearn.model_selection import train_test_split

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=42, stratify=df['target']
    )
    df = df.copy()
    df['split'] = 'train'
    df.loc[test_idx, 'split'] = 'test'
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert (output['split'] == 'test').sum() == 30
