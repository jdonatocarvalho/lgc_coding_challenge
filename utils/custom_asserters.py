from utils.basic_logger import Logger


def assert_true(value):
    assert value, 'Value {} not true or does not exist'.format(value)
    Logger.debug('Assertion successful: Value {} exists'.format(value))


def assert_equal(value, reference):
    assert value == reference, 'Actual value {} is NOT equal to excpected {}'.format(value, reference)
    Logger.debug('Actual value {} is equal to expected {}!'.format(value, reference))