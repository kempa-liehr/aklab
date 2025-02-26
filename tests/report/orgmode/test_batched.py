from aklab.report.orgmode import batched

def test_even():
    my_list = [1, 2, 3, 4]
    out_list = list(batched(my_list))
    assert out_list == [[1, 2], [3, 4]]

def test_odd():
    my_list = [1, 2, 3, 4, 5]
    out_list = list(batched(my_list))
    assert out_list == [[1, 2], [3, 4], [4, 5]]

def test_batch_size():
    my_list = [1, 2, 3, 4, 5]
    out_list = list(batched(my_list, n=3))
    assert out_list == [[1, 2, 3], [3, 4, 5]]
