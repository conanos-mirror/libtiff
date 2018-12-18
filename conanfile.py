from conans import ConanFile, CMake, tools
from conanos.build import config_scheme
import os

class LibtiffConan(ConanFile):
    name = "libtiff"
    version = "4.0.10"
    description = "TIFF(Tag Image File Format) Library and Utilities"
    url = "https://github.com/conanos/libtiff"
    homepage = "http://www.libtiff.org/"
    license = "BSD"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        'fPIC': [True, False]
    }
    default_options = { 'shared': True, 'fPIC': True }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def source(self):
        url_ = "https://gitlab.com/libtiff/libtiff/-/archive/v{version}/libtiff-v{version}.tar.gz"
        tools.get(url_.format(version=self.version))
        extracted_dir = self.name + "-v" + self.version
        os.rename(extracted_dir, self._source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        cmake.build()
        cmake.test()
        cmake.install()

    def package(self):
        if self.options.shared:
            replacements = {"-ltiff": "-ltiffd"}
            for s, r in replacements.items():
                tools.replace_in_file(os.path.join(self.package_folder,"lib","pkgconfig", "libtiff-4.pc"),s,r)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

