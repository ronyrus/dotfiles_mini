#!/usr/bin/env python2
import sys
import os
import platform
import glob
import subprocess
import logging
import shutil
import stat
import zipfile
from cli import CommandLineApp, Argument, Command
import subprocess as sb

system_str = platform.system()
home_dir = os.path.expanduser('~')
base_dir = os.path.dirname(os.path.abspath(__file__))

def is_mac():
    return 'Darwin' in system_str

def is_linux():
    return 'Linux' in system_str

def is_bash():
    env_sh = os.environ["SHELL"]
    return env_sh != "" and env_sh.endswith("bash")

def plat_suffix():
    if is_linux(): return 'lin'
    elif is_mac(): return 'mac'

logging.basicConfig(level='WARN')
log = logging.getLogger("DotManager")

class DotManager(CommandLineApp):
    """ Dot files manager """
    # DEFAULT_REPO_PATH = os.path.dirname(__file__)

    # _config = Argument("-c", "--config", help="Select a configuration file", default="packages.txt")
    # _path = Argument("--path", help="Select alternative repo path", default=DEFAULT_REPO_PATH)
    _verbosity = Argument('-v', '--verbose', action="count", help="Be more verbose")

    def __init__(self):
        if self._verbosity >= 1:
            log.setLevel(logging.DEBUG)


    # @Argument("-i", "--ignore-errors", action="store_true", help="Ignore recoverable errors")
    @Argument("module", default='', nargs='?', help="link a specific module")
    @Argument("-l", "--list", dest='lst', action="store_true", help="list modules")
    @Command
    def link(self, lst, module):
        """ Link dot files into repository """
        log.info('linking dotfiles...')
        modules = ['git', 'tmux', 'nix', 'bash', 'vim']

        if lst:
            print modules
            return

        if module:
            if module in modules:
                modules = [module]
            else:
                log.error("unknown module %s" % module)
                return

        linkables = []
        for d in modules:
            linkables += glob.glob(os.path.join(d, '*.' + 'always'))
            linkables += glob.glob(os.path.join(d, '*.' + plat_suffix()))

        for l in linkables:

            source_file = os.path.join(base_dir, l)
            file_name = os.path.basename(l)
            target_file = os.path.join(home_dir, '.' + os.path.splitext(file_name)[0])
            log.debug('symlink:%s --> %s', target_file, source_file)

            if os.path.exists(target_file):
                os.remove(target_file)
            os.symlink(source_file, target_file)

    @Command
    def fonts(self):
        """ Install fonts """
        fonts_source = os.path.join(base_dir, 'fonts')

        if is_mac():
            fonts_target = os.path.join(home_dir, 'Library', 'Fonts', 'dotfiles_fonts')
        elif is_linux():
            fonts_target = os.path.join(home_dir, '.fonts', 'dotfiles_fonts')
        else:
            log.error('platform is not supported')
            raise

        log.debug('linking fonts: %s --> %s', fonts_target, fonts_source)
        if os.path.exists(fonts_target):
            os.remove(fonts_target)
        try:
            parent_dir = os.path.dirname(fonts_target)
            os.makedirs(parent_dir)
        except OSError as e:
            if e.errno == 17: # File exists
                log.debug("dir [%s] already exists ..." % parent_dir)
            else:
                raise e
        os.symlink(fonts_source, fonts_target)

        if is_linux():
            log.debug('updating font cache...')
            sb.call(('fc-cache -fv %s' % fonts_target).split(), stdout=dev_null, stderr=dev_null)



if __name__ == '__main__':
    DotManager.run()


#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================

# def size(num):
#     if num < 1024 * 1024:
#         return "%0.2f kB" % (num / 1024.)
#     if num < 1024 * 1024 * 1024:
#         return "%0.2f MB" % (num / 1024. / 1024)
#     else:
#         return "%0.2f GB" % (num / 1024. / 1024 / 1024)

# def parents(path, root=None):
#     """ Yield all parent directories up to root, exclusive (if specified) """
#     path = os.path.abspath(path)

#     while root is None or path.startswith(root) and path != root:
#         yield path
#         if path == os.path.dirname(path):
#             break
#         path = os.path.dirname(path)


# class Repository(object):
#     APPNAME = 'ios_team'
#     GIT_PATH = "git"

#     def __init__(self, name, path, origin, ref):
#         self.logger = logging.getLogger("RepoManager.repo")
#         self.name = name
#         self.path = path
#         self.origin = origin
#         self.ref = ref

#     def _git_command(self, args):
#         if self.exists:
#             cwd = self.path
#         else:
#             cwd = '.'
#         cmd = [self.GIT_PATH] + list(args)
#         self.logger.debug("%s, cwd=%s", " ".join(cmd), cwd)
#         return subprocess.check_output(cmd, cwd=cwd)

#     def create(self, shallow=False):
#         self.logger.debug("Cloning %s from %s", self.name, self.origin)
#         if shallow:
#             shargs = ['--depth', '1']
#         else:
#             shargs = []
#         args = ['clone', '-n'] + shargs + [self.origin, self.path]
#         self._git_command(args)

#     def update(self, force=False):
#         if not self.exists:
#             raise ValueError("Repository %s doesn't exist" % self.name)
#         self._git_command(['remote', 'set-url', 'origin', self.origin])
#         self._git_command(['fetch', '-a'])
#         if self.status() != "clean":
#             if not force:
#                 self.logger.warn("Repository %s has uncommitted changes, use -f to force update", self.name)
#                 return
#         self._git_command(['checkout', '-qf', self.ref])

#         try:
#             self._git_command(['show-ref', '--verify', "refs/heads/%s" % self.ref])
#         except:
#             self.logger.info("Repository in detached head")
#             return

#         # preform ff only merge
#         try:
#             self.logger.info("Fast-forwarding local branch")
#             self._git_command(['merge', '--ff-only', self.ref, 'origin/%s' % self.ref])
#         except:
#             raise RuntimeError("Failed fast-forward on repository %s" % self.name)

#     def status(self):
#         if not self.exists:
#             return "<missing>"
#         status = self._git_command(['status', '--porcelain']).strip()
#         self.logger.debug("  %s status:\n%s", self.name, status)
#         if not status:
#             return 'clean'
#         else:
#             return status

#     def get_head(self):
#         """ Get the name of the HEAD commit """
#         if not self.exists:
#             raise ValueError("Repository %s doesn't exist" % self.name)
#         ref = self._git_command(["show-ref", "HEAD"]).strip().split()[0]
#         return ref

#     @property
#     def exists(self):
#         return os.path.exists(os.path.join(self.path, '.git'))


# class RepoManager(CommandLineApp):
#     """ ios_team repository manager / helper """
#     DEFAULT_REPO_PATH = os.path.dirname(__file__)

#     _config = Argument("-c", "--config", help="Select a configuration file", default="packages.txt")
#     _path = Argument("--path", help="Select alternative repo path", default=DEFAULT_REPO_PATH)
#     _verbosity = Argument('-v', '--verbose', action="count", help="Be more verbose")

#     def __init__(self):
#         logging.basicConfig(level='WARN')
#         self.logger = logging.getLogger("RepoManager")
#         verbosity = min(2, (self._verbosity or 0))
#         self._path = os.path.abspath(self._path or '.')
#         self.logger.setLevel(30 - verbosity * 10)
#         self.repositories = []

#         for name, origin, ref in self._load_config():
#             path = os.path.abspath(os.path.join(self._path, *name.split(".")))
#             if any(path.startswith(x.path) or x.path.startswith(path) for x in self.repositories):
#                 raise ValueError("Nested repositories found: %s" % path)
#             if not path.startswith(self._path):
#                 raise ValueError("Invalid repository path: %s" % path)
#             repo = Repository(name, path, origin, ref)
#             self.repositories.append(repo)

#     def _load_config(self):
#         """ Read the configuration file and yield tuples of (subpath, origin, ref) for each repository """
#         self.logger.info("Using config file %s", self._config)
#         with open(self._config) as f:
#             for i, line in enumerate(f):
#                 line = line.strip()
#                 if not line or line.startswith('#'):
#                     continue
#                 fields = line.split()
#                 if len(fields) != 3:
#                     raise ValueError("Invalid repository specification in line %d" % i)
#                 yield fields

#     @Argument("-i", "--ignore-errors", action="store_true", help="Ignore recoverable errors")
#     @Argument("-f", "--force", action="store_true", help="Discard local uncommitted changes")
#     @Command
#     def update(self, ignore_errors=False, force=False):
#         """ Update all repositories in tree """
#         for repo in self.repositories:
#             repo_force = force
#             try:
#                 if not repo.exists:
#                     self.logger.info('Creating missing repository %s', repo.name)
#                     repo_force = True  # make sure to update anyway since clone doesn't checkout
#                     repo.create()

#                 self.logger.info('Updating %s to %s', repo.name, repo.ref)
#                 repo.update(repo_force)

#                 # Create all __init__.py's
#                 for path in parents(os.path.dirname(repo.path), self._path):
#                     f = os.path.join(path, '__init__.py')
#                     if not os.path.exists(f):
#                         self.logger.info("create %s", f)
#                         open(f, 'w').close()
#                     path = os.path.dirname(path)
#             except Exception as e:
#                 if not ignore_errors:
#                     raise
#                 else:
#                     self.logger.error("Failed updating %s: %s", repo.name, e)


#     @Argument("-F", "--force", action="store_true", help="JUST DO IT")
#     @Command
#     def delete(self, force):
#         """ delete all repositories """
#         if not self.initialized:
#             print "Not initialized. Use update."
#             return 1
#         # On Windows git sets readonly flag so we need to turn that off if we can't delete something
#         roots = set()
#         def err(f, path, exc):
#             if os.path.exists(path):
#                 os.chmod(path, stat.S_IWRITE)
#                 f(path)
#         # find the shared roots
#         for repo in self.repositories:
#             if repo.exists and repo.status() != 'clean':
#                 self.logger.warn("repository %s is not clean", repo.name)
#             roots.add(list(parents(repo.path, self._path))[-1])
#         # Delete all directories
#         for d in roots:
#             if not force and raw_input("Delete %s? (y/n) " % d).lower().startswith('y'):
#                 self.logger.info("Deleting %s", d)
#                 shutil.rmtree(d, onerror=err)
#             else:
#                 self.logger.info("Skipping %s", d)


#     @Command
#     def status(self):
#         """ Show repository status

#         Shows the status of each repository in the tree
#         """
#         if not self.initialized:
#             print "Not initialized. Use update."
#             return
#         for repo in self.repositories:
#             print "%s:" % os.path.relpath(repo.path, self._path), repo.status()

#     @Argument("-o", "--output", help="Select file to output")
#     @Command
#     def freeze(self, output=None):
#         """Save current repository state

#         Outputs to stdout by default. Use the output argument to write to file.
#         """
#         if output is None:
#             output = sys.stdout
#         else:
#             output = open(output, 'wb')
#         for repo in self.repositories:
#             output.write("%s %s %s\n" % (repo.name, repo.origin, repo.get_head()))

#     @Command
#     def list(self):
#         """ List the packages in the tree"""
#         print "Available packages:"
#         for repo in self.repositories:
#             print '*', repo.name

#     def _get_site(self, systemwide=False):
#         import site
#         if systemwide:
#             self.logger.warn("Modifying global Python installation")
#             return site.getsitepackages()[0]
#         else:
#             return site.getusersitepackages()

#     @Argument("-g", "--global", dest='systemwide', action="store_true", help="Install globally for all users")
#     @Command
#     def install(self, systemwide):
#         " Install the directory so it can be imported from "
#         path = self._get_site(systemwide)
#         if not os.path.exists(path):
#             os.makedirs(path)
#         open(os.path.join(path, 'ios_team.pth'), 'wb').write(self._path)
#         self.logger.info("Installed to path")

#     @Argument("-g", "--global", dest='systemwide', action="store_true", help="Uninstall globally for all users")
#     @Command
#     def uninstall(self, systemwide):
#         " Uninstall ios_team from Python path "
#         path = self._get_site(systemwide)
#         f = os.path.join(path, 'ios_team.pth')
#         if os.path.exists(f):
#             os.unlink(f)
#         self.logger.info("Uninstalled from path")

#     @Argument("-d", "--dest", help="Destination path, can be a zip filename or a directory")
#     @Argument("-f", "--format", help="Package format, currently supported: zip")
#     @Command
#     def package(self, format, dest):
#         " Create package "
#         if format is not None and format.lower != 'zip':
#             raise ValueError("Format unsupported: %s" % format)
#         if dest is None:
#             dest = os.path.join(self._path, "dist", "ios_team.zip")

#         if not os.path.exists(dest):
#             if not os.path.exists(os.path.dirname(dest)):
#                 os.makedirs(os.path.dirname(dest))
#         elif os.path.isdir(dest):
#             dest = os.path.join(dest, "ios_team.zip")

#         self.logger.info("Saving distribution package", dest)
#         with zipfile.ZipFile(dest, "w") as zf:
#             for repo in self.repositories:
#                 for path, dirs, files in os.walk(repo.path):
#                     if '.git' in path:
#                         continue
#                     for f in files:
#                         if f.endswith('.pyc'):
#                             continue
#                         fn = os.path.join(path, f)
#                         zf.write(fn, os.path.relpath(fn, self._path))
#         print '%s\t%s' % (dest, size(os.stat(dest).st_size))
#         self.logger.info("Done")

#     @property
#     def initialized(self):
#         return any(x.exists for x in self.repositories)

# if __name__ == '__main__':
#     RepoManager.run()

