import path from 'node:path';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [react()],
	build: {
		outDir: 'dist',
		assetsDir: 'assets',
		sourcemap: false,
		minify: 'terser',
		rollupOptions: {
			output: {
				manualChunks: undefined,
			},
		},
	},
	server: {
		port: 5173,
		host: true,
	},
	preview: {
		port: 3000,
		host: true,
	},
	resolve: {
		extensions: ['.jsx', '.js', '.tsx', '.ts', '.json'],
		alias: {
			'@': path.resolve(__dirname, './src'),
		},
	},
});
