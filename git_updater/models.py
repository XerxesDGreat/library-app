__author__ = 'josh'

class Version(object):
    def __init__(self, major_version=0, minor_version=0, patch_version=0, label=""):
        self.major_version = major_version
        self.minor_version = minor_version
        self.patch_version = patch_version
        self.label = label

    def __eq__(self, other):
        self._assert_version_obj(other)
        return self.major_version == other.major_version \
            and self.minor_version == other.minor_version \
            and self.patch_version == other.patch_version \
            and self.label == other.label

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self.major_version > other.major_version:
            return True
        elif self.major_version < other.major_version:
            return False
        else:
            if self.minor_version > other.minor_version:
                return True
            elif self.minor_version < other.minor_version:
                return False
            else:
                if self.patch_version > other.patch_version:
                    return True
                elif self.patch_version < other.patch_version:
                    return False
                else:
                    return self.label.lower() > other.label.lower()

    def __lt__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return not self.__ge__(other)

    def _assert_version_obj(self, version):
        if not isinstance(version, Version):
            raise TypeError('must provide Version object')

    @classmethod
    def from_string(cls, version_string):
        if '-' in version_string:
            version, label = version_string.split('-')
        else:
            version = version_string
            label = ''
        version_parts = version.split('.')
        try:
            major = int(version_parts[0].lstrip('v'))
        except:
            major = 0

        try:
            minor = int(version_parts[1])
        except:
            minor = 0

        try:
            patch = int(version_parts[2])
        except:
            patch = 0

        return cls(major_version=major, minor_version=minor, patch_version=patch, label=label)

    def __str__(self):
        return '-'.join(['%d.%d.%d' % (self.major_version, self.minor_version, self.patch_version), self.label])