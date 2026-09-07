"""Synthetic coverage for the post-hoc element-pair stability diagnostics."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import analyze_element_pair as base_analysis
import analyze_element_pair_stability as stability_analysis
import test_system_holdout_analysis as system_fixture


class ElementPairStabilityAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        system_fixture.SystemAnalysisTests.setUpClass()
        cls.base=system_fixture.SystemAnalysisTests.base
        for script,target in (('run_element_pair.jl','primary'),('run_element_pair_stability.jl','stability')):
            command=['julia','--startup-file=no',f'--project={ROOT}',str(ROOT/'scripts'/script),'snapshot','audit','results',target,'--synthetic']
            result=subprocess.run(command,cwd=cls.base,text=True,capture_output=True)
            if result.returncode:raise RuntimeError(result.stdout+result.stderr)

    @classmethod
    def tearDownClass(cls):system_fixture.SystemAnalysisTests.tearDownClass()

    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.path=Path(temp.name)
        self.primary=self.path/'primary';self.stability=self.path/'stability'
        shutil.copytree(self.base/'primary',self.primary);shutil.copytree(self.base/'stability',self.stability)

    def test_complete_hashed_analysis_and_no_overwrite(self):
        output=self.path/'analysis';summary=stability_analysis.analyze(self.primary,self.stability,output)
        self.assertEqual(summary['fits'],18)
        self.assertEqual(json.loads((output/'validation.json').read_text())['status'],'passed')
        manifest=json.loads((output/'SHA256SUMS.json').read_text())
        self.assertEqual(set(manifest['files']),{p.relative_to(output).as_posix() for p in output.iterdir() if p.name!='SHA256SUMS.json'})
        with self.assertRaisesRegex(ValueError,'overwrite'):stability_analysis.analyze(self.primary,self.stability,output)

    def test_rejects_wrong_stability_mode(self):
        config=self.stability/'config.toml'
        config.write_text(config.read_text().replace('analysis_mode = "posthoc_stability_20000"','analysis_mode = "invented"'))
        with self.assertRaisesRegex(ValueError,'analysis mode'):stability_analysis.analyze(self.primary,self.stability,self.path/'analysis')

    def test_rehashed_ranking_corruption_is_detected(self):
        name='composition/original/split-00/ranking.tsv';path=self.stability/name
        old=base_analysis.sha(path);data=base_analysis.rows(path);data[0]['score']='123';path.unlink();base_analysis.write_rows(path,data)
        config=self.stability/'config.toml';config.write_text(config.read_text().replace(f'"{name}" = "{old}"',f'"{name}" = "{base_analysis.sha(path)}"'))
        with self.assertRaisesRegex(ValueError,'factor score'):stability_analysis.analyze(self.primary,self.stability,self.path/'analysis')


if __name__=='__main__':unittest.main()
