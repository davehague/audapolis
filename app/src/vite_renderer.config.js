import { defineConfig } from 'vite';
import { escapeRegExp } from 'lodash';
import react from '@vitejs/plugin-react';
import { builtinModules } from 'module';
import pkg from '../package.json';
import commonjsExternals from 'vite-plugin-commonjs-externals';

const commonjsPackages = [
  'electron',
  'electron/main',
  'electron/common',
  'electron/renderer',
  'original-fs',
  ...builtinModules,
  ...Object.keys(pkg.dependencies).map(
    (name) => new RegExp('^' + escapeRegExp(name) + '(\\/.+)?$')
  ),
];

export default defineConfig({
  root: __dirname,
  base: '',
  plugins: [react(), commonjsExternals({ externals: commonjsPackages })],
  build: {
    outDir: '../build/renderer_process/',
    emptyOutDir: true,
    minify: false,
    // brotliSize removed in Vite 6
  },
});
