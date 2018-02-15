{-# LANGUAGE CPP #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
{-# OPTIONS_GHC -fno-warn-implicit-prelude #-}
module Paths_Alice (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [2,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/bin"
libdir     = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/lib/x86_64-linux-ghc-8.2.2/Alice-2.0-Az9WWccddtCL8d7Tf9XJcN"
dynlibdir  = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/lib/x86_64-linux-ghc-8.2.2"
datadir    = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/share/x86_64-linux-ghc-8.2.2/Alice-2.0"
libexecdir = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/libexec/x86_64-linux-ghc-8.2.2/Alice-2.0"
sysconfdir = "/home/la1/Documents/MasterThesis/aiw2/.cabal-sandbox/etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "Alice_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "Alice_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "Alice_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "Alice_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "Alice_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "Alice_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
