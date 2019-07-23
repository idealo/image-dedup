from imagededup.evaluation.performance import Metrics
import os
import pickle
import pytest
"""Run from project root with: python -m pytest -vs tests/test_evaluation_logic.py --cov=imagededup.evaluation"""


def load_pickle(filename):
    """The path of the file below is set since the test suite is run using python -m pytest command from the image-dedup
    directory"""
    with open(os.path.join('tests', 'data', filename), 'rb') as f:
        dict_loaded = pickle.load(f)
    return dict_loaded


def run_before_main_metrics(ground_truth_file, retrieval_file):
    """Loads ground truth and retrieval dicts, declares an eval object, returns initialized object"""
    dict_ground_truth = load_pickle(ground_truth_file)
    dict_retrievals = load_pickle(retrieval_file)
    evalobj = Metrics(dict_ground_truth, dict_retrievals)
    return evalobj


def initialize_fake_data_retrieved_same():
    """Number of retrievals = Number of ground truth retrievals"""
    corr_dup = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
    ret_dups = ['1.jpg', '33.jpg', '2.jpg', '4.jpg']
    return corr_dup, ret_dups


def initialize_fake_data_retrieved_less():
    """Number of retrievals < Number of ground truth retrievals"""
    corr_dup = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
    ret_dups = ['1.jpg', '42.jpg']
    return corr_dup, ret_dups


def initialize_fake_data_retrieved_more():
    """Number of retrievals > Number of ground truth retrievals"""
    corr_dup = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
    ret_dups = ['1.jpg', '42.jpg', '2.jpg', '3.jpg', '4.jpg']
    return corr_dup, ret_dups


def test_avg_prec_same():
    """Number of retrievals = Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_same()
    av_prec_val = Metrics.avg_prec(corr_dup, ret_dups)
    assert av_prec_val == 0.6041666666666666


def test_ndcg_same():
    """Number of retrievals = Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_same()
    ndcg_val = Metrics.ndcg(corr_dup, ret_dups)
    assert ndcg_val == 0.75369761125927


def test_jaccard_same():
    """Number of retrievals = Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_same()
    jac_val = Metrics.jaccard_similarity(corr_dup, ret_dups)
    assert jac_val == 0.6


def test_avg_prec_less():
    """Number of retrievals < Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_less()
    av_prec_val = Metrics.avg_prec(corr_dup, ret_dups)
    assert av_prec_val == 0.25


def test_ndcg_less():
    """Number of retrievals < Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_less()
    ndcg_val = Metrics.ndcg(corr_dup, ret_dups)
    assert ndcg_val == 0.6131471927654584


def test_jaccard_less():
    """Number of retrievals < Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_less()
    jac_val = Metrics.jaccard_similarity(corr_dup, ret_dups)
    assert jac_val == 0.2


def test_avg_prec_retrieved_more():
    """Number of retrievals > Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_more()
    av_prec_val = Metrics.avg_prec(corr_dup, ret_dups)
    assert av_prec_val == 0.8041666666666667


def test_ndcg_retrieved_more():
    """Number of retrievals > Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_more()
    ndcg_val = Metrics.ndcg(corr_dup, ret_dups)
    assert ndcg_val == 0.9047172294870751


def test_jaccard_retrieved_more():
    """Number of retrievals > Number of ground truth retrievals"""
    corr_dup, ret_dups = initialize_fake_data_retrieved_more()
    jac_val = Metrics.jaccard_similarity(corr_dup, ret_dups)
    assert jac_val == 0.8


def test_map_is_1_for_all_correct():
    """Tests if correct MAP values are computed
    Load ground truth and dict for all correct map prediction to have a Map of 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'all_correct_retrievals.pkl')
    map_func = evalobj.avg_prec
    map_val = evalobj.mean_all_func(map_func)
    assert map_val == 1.0


def test_map_is_not_1_for_incorrect():
    """Tests if correct MAP values are computed
    Load ground truth and dict for incorrect map prediction to have a Map less than 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    map_func = evalobj.avg_prec
    map_val = evalobj.mean_all_func(map_func)
    assert map_val == 0.5555555555555556


def test_jaccard_is_1_for_all_correct():
    """Tests if correct Jaccard similarity values are computed
    Load ground truth and dict for all correct retrievals for Jaccard similarity to have a value of 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'all_correct_retrievals.pkl')
    jac_func = evalobj.jaccard_similarity
    jac_val = evalobj.mean_all_func(jac_func)
    assert jac_val == 1.0


def test_jaccard_is_not_1_for_incorrect():
    """Tests if correct average Jaccard similarity values are computed
    Load ground truth and dict for incorrect retrievals to have a average Jaccard similarity of less than 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    jac_func = evalobj.jaccard_similarity
    jac_val = evalobj.mean_all_func(jac_func)
    assert jac_val == 0.6


def test_ndcg_is_1_for_all_correct():
    """Tests if correct average ndcg values are computed
    Load ground truth and dict for all correct retrievals for Jaccard similarity to have a value of 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'all_correct_retrievals.pkl')
    ndcg_func = evalobj.ndcg
    ndcg_val = evalobj.mean_all_func(ndcg_func)
    assert ndcg_val == 1.0


def test_ndcg_is_not_1_for_incorrect():
    """Tests if correct average ndcg values are computed
    Load ground truth and dict for incorrect retrievals to have a average ndcg of less than 1.0"""
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    ndcg_func = evalobj.ndcg
    ndcg_val = evalobj.mean_all_func(ndcg_func)
    assert ndcg_val == 0.6173196815056892


def test_get_metrics_returns_dict():
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    assert isinstance(evalobj.get_all_metrics(), dict)


def test_get_metrics_not_empty():
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    metrics_dict = evalobj.get_all_metrics()
    metrics_dict_vals = metrics_dict.values()
    assert len(metrics_dict_vals)


def test_get_metrics_save():
    if os.path.exists('all_average_metrics.pkl'):
        os.remove('all_average_metrics.pkl')
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    evalobj.get_all_metrics()
    assert os.path.exists('all_average_metrics.pkl')


def test_get_metrics_does_not_save_when_save_false():
    if os.path.exists('all_average_metrics.pkl'):
        os.remove('all_average_metrics.pkl')
    evalobj = run_before_main_metrics('ground_truth.pkl', 'incorrect_retrievals.pkl')
    evalobj.get_all_metrics(save=False)
    assert not os.path.exists('all_average_metrics.pkl')


@pytest.mark.parametrize('metric_func', [Metrics.avg_prec, Metrics.ndcg, Metrics.jaccard_similarity])
def test_zero_retrieval(metric_func):
    corr_dup = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
    ret_dups = []
    av_val = metric_func(corr_dup, ret_dups)
    assert av_val == 0.0
