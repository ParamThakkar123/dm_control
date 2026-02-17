# Copyright 2026 The dm_control Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Tests for OpenGL backend import behavior."""

import os

from absl.testing import absltest
from dm_control import _render


class BackendImportTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self._platform_env_name = _render.constants.PYOPENGL_PLATFORM
    self._old_platform_env = os.environ.get(self._platform_env_name)

  def tearDown(self):
    if self._old_platform_env is None:
      os.environ.pop(self._platform_env_name, None)
    else:
      os.environ[self._platform_env_name] = self._old_platform_env
    super().tearDown()

  def testImportFailureRestoresMissingPyOpenGLPlatform(self):
    os.environ.pop(self._platform_env_name, None)

    def failing_import():
      os.environ[self._platform_env_name] = _render.constants.EGL[0]
      raise ImportError('EGL unavailable')

    with self.assertRaises(ImportError):
      _render._import_with_env_restore(failing_import)

    self.assertNotIn(self._platform_env_name, os.environ)

  def testImportFailureRestoresExistingPyOpenGLPlatform(self):
    os.environ[self._platform_env_name] = _render.constants.OSMESA[0]

    def failing_import():
      os.environ[self._platform_env_name] = _render.constants.EGL[0]
      raise ImportError('EGL unavailable')

    with self.assertRaises(ImportError):
      _render._import_with_env_restore(failing_import)

    self.assertEqual(
        _render.constants.OSMESA[0], os.environ[self._platform_env_name])


if __name__ == '__main__':
  absltest.main()
