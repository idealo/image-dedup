import os

from click.testing import CliRunner
from imagededup.client.client import find_duplicates

PATH_IMAGE_DIR = 'tests/data/mixed_images'
FILENAME = 'tests/test_output.json'


def test_no_image_dir_given():
    runner = CliRunner()
    result = runner.invoke(find_duplicates, ['--image_dir', ''])
    assert result.exit_code == 2


def test_image_dir_given_but_no_method():
    runner = CliRunner()
    result = runner.invoke(find_duplicates, ['--image_dir', PATH_IMAGE_DIR])
    assert result.exit_code == 2


def test_image_dir_given_and_method():
    runner = CliRunner()
    result = runner.invoke(find_duplicates, ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash'])
    assert result.exit_code == 0


def test_image_dir_given_but_wrong_method():
    runner = CliRunner()
    result = runner.invoke(find_duplicates, ['--image_dir', PATH_IMAGE_DIR, '--method', 'LHash'])
    assert result.exit_code == 2


def test_file_is_created():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--outfile', FILENAME])
    assert result.exit_code == 0
    assert os.path.isfile(FILENAME) is True
    # cleanup
    os.remove(FILENAME)


def test_hash_max_distance_threshold_int():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '20'])
    assert result.exit_code == 0


def test_hash_max_distance_threshold_no_int():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '0.5'])
    assert result.exit_code == 2


def test_hash_max_distance_threshold_in_range_left_interval():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '0'])
    assert result.exit_code == 0


def test_hash_max_distance_threshold_in_range_right_interval():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '64'])
    assert result.exit_code == 0


def test_hash_max_distance_threshold_out_of_range_negative():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '-30'])
    assert result.exit_code == 2


def test_hash_max_distance_threshold_out_of_range_positive():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '900'])
    assert result.exit_code == 2


def test_hash_min_similarity_threshold_has_no_effect():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--min_similarity_threshold', '0.5'])
    assert result.exit_code == 0


def test_cnn_min_similarity_threshold_float():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '0.5'])
    assert result.exit_code == 0


def test_cnn_min_similarity_threshold_no_float():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '10'])
    assert result.exit_code == 2


def test_cnn_min_similarity_threshold_in_range_left_interval():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '-1.0'])
    assert result.exit_code == 0


def test_cnn_min_similarity_threshold_in_range_right_interval():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '1.0'])
    assert result.exit_code == 0


def test_cnn_min_similarity_threshold_out_of_range_negative():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '-1.5'])
    assert result.exit_code == 2


def test_cnn_min_similarity_threshold_out_of_range_positive():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'CNN', '--min_similarity_threshold', '1.5'])
    assert result.exit_code == 2


def test_cnn_max_distance_threshold_has_no_effect():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--max_distance_threshold', '10'])
    assert result.exit_code == 0


def test_scores_boolean():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--scores', 'False'])
    assert result.exit_code == 0


def test_scores_no_boolean():
    runner = CliRunner()
    result = runner.invoke(find_duplicates,
                           ['--image_dir', PATH_IMAGE_DIR, '--method', 'PHash', '--scores', 'hello'])
    assert result.exit_code == 2
