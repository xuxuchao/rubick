"""
用例运行入口
@filename: search_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import os
import sys
import time
import pickle
import unittest
from optparse import OptionParser

from utils.html_runner import HTMLTestRunner
from utils.config import Config, PROJECT_ROOT
from utils.log import logging, log_action
from utils.send_email import send_email
from utils.device import Device

TEST_CASE_PATH = os.path.join(PROJECT_ROOT, 'test_case')
LAST_FAILS = 'last_fails.suite'  # 用于存储上次失败的用例suite的序列化文件

# 命令行选项
parser = OptionParser()

parser.add_option('--collect-only', action='store_true', dest='collect_only', help='仅列出所有用例')
parser.add_option('--rerun-fails', action='store_true', dest='rerun_fails', help='运行上次失败的用例')
parser.add_option('--tag', action='store', dest='tag', help='运行指定tag的用例')
parser.add_option('--app', action='store', dest='app', help='指定的app平台')
parser.add_option('--device', action='store', dest='device', help='使用指定的设备')
parser.add_option('--hub', action='store', dest='hub', help='指定Appium Server')

(options, args) = parser.parse_args()  # 应用选项（使生效）


@log_action
def discover():
    return unittest.defaultTestLoader.discover(TEST_CASE_PATH)


@log_action
def save_failures(result, file):
    suite = unittest.TestSuite()
    for case_result in result.failures:
        suite.addTest(case_result[0])

    with open(file, 'wb') as f:
        pickle.dump(suite, f)


def collect():
    suite = unittest.TestSuite()

    def _collect(tests):
        if isinstance(tests, unittest.TestSuite):
            if tests.countTestCases() != 0:
                for i in tests:
                    _collect(i)
        else:
            suite.addTest(tests)

    _collect(discover())
    return suite


@log_action
def makesuite_by_tag(tag):
    suite = unittest.TestSuite()
    for case in collect():
        if case._testMethodDoc and tag in case._testMethodDoc:
            suite.addTest(case)

    return suite


@log_action
def run(suite):
    start_time = time.time()
    logging.info("{} 测试开始 {}".format("="*25, "="*25))
    report_config = Config.get_report_config()
    report_dir = report_config.get("report_dir") or 'report'
    report_title = report_config.get("report_title") or "Test Report"
    report_description = report_config.get("report_description") or ""
    run_config = Config.get_run_config()
    is_send_email = run_config.get('is_send_email')

    # task_dir = Config.task_dir
    # report_file = os.path.join(task_dir, 'report.html')
    # now = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    # report_file = os.path.join(PROJECT_ROOT, report_dir, 'report_{}.html'.format(now))
    report_file = os.path.join(PROJECT_ROOT, report_dir, 'report.html')
    # 录制屏幕
    # os.popen('adb shell screenrecord /sdcard/record.mp4')

    with open(report_file, 'wb') as f:  # 从配置文件中读取
        result = HTMLTestRunner(stream=f, title=report_title, description=report_description).run(suite)

    # 下载录制文件
    # os.system('adb pull /sdcard/record.mp4 {}'.format(task_dir))

    last_fails_file = 'last_fails.suite'
    if result.failures:
        save_failures(result, last_fails_file)

    if is_send_email:
        send_email()

    case_num = suite.countTestCases()
    duration = time.time() - start_time
    logging.info("{} 测试结束 执行用例:{} 用时: {:.3f}s {}".format("="*10, case_num, duration, "="*10))


@log_action
def collect_only():
    t0 = time.time()
    i = 0
    for case in collect():
        i += 1
        print("{}.{}".format(str(i), case.id()))
    # print("{:^10}".format("_"))
    print("-" * 50)
    print("Collect {} tests is {:.3f}s".format(str(i), time.time()-t0))


def run_all():
    run(discover())


def run_by_tag(tag):
    run(makesuite_by_tag(tag))


def rerun_fails():
    sys.path.append(TEST_CASE_PATH)
    with open(LAST_FAILS, 'rb') as f:
        suite = pickle.load(f)
    run(suite)


def main():
    if options.app:
        Config.app = options.app

    if options.device:
        Config.device = options.device

    if options.hub:
        Config.hub = options.hub

    if options.collect_only:
        collect_only()
    elif options.rerun_fails:
        rerun_fails()
    elif options.tag:
        run(makesuite_by_tag(options.tag))
    else:
        run_all()


if __name__ == '__main__':
    main()

