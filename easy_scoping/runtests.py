import os
import sys



def run_tests():

    test_dir = os.path.dirname(__file__)
    sys.path.insert(0, test_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'easy_scoping.settings'

    import django
    from django.conf import settings
    from django.test.utils import get_runner

    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)

    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
