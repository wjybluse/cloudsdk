__author__ = 'wan'
# auto scale via 3rd party tool
# current support ali,aws
# ali ess is not stable
# add scale group
# scale out
# scale in
class AutoScaling():
    def __init__(self):
        pass

    def add_autoscaling_group(self, name, instance=None, policy=None, max_instance=3, min_instance=0):
        """
        :param name:scale group name
        :param instance: instance id
        :param policy: scale policy
        :param max_instance:max instance in group
        :param min_instance:min instance in group
        :return:
        """
        pass

    def remove_autoscaling_group(self, group):
        """
        :param group:group id
        :return:
        """
        pass

    def scale_out(self):
        """
        :return:can do it auto?
        """
        pass

    def scale_in(self):
        """
        :return:can do it auto?
        """
        pass