#!/usr/bin/env python2.7
#changed the python version from 2 to 2.7

import argparse
import json
import sys
import subprocess
import tempfile

from ingredient_phrase_tagger.training import utils


def _exec_crf_test(input_text, model_path):
    with tempfile.NamedTemporaryFile() as input_file:
        input_file.write(utils.export_data(input_text))
        input_file.flush()
        return subprocess.check_output(
            ['crf_test', '--verbose=1', '--model', model_path,
             input_file.name]).decode('utf-8')


def _convert_crf_output_to_json(crf_output):
    return json.dumps(utils.import_data(crf_output), indent=2, sort_keys=True)


def main(args):
    raw_ingredient_lines = [x for x in sys.stdin.readlines() if x]
    crf_output = _exec_crf_test(raw_ingredient_lines, args.model_file)
    print _convert_crf_output_to_json(crf_output.split('\n'))


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    parser = argparse.ArgumentParser(
        prog='Ingredient Phrase Tagger',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model-file', required=True)
    main(parser.parse_args())
