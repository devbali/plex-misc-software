from gen_from_ballots import run_file
import filecmp

class TestFull:
    def test_one(self, tmp_path):
        run_file("test_ballots/test_ballot1.tsv", graphout = tmp_path, printout=tmp_path/"test_out.txt")
        assert filecmp.cmp(tmp_path/"test_out.txt", "test_graphs/expected.txt")
