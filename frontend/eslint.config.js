import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";
import pluginJsxA11y from "eslint-plugin-jsx-a11y";
import pluginImport from "eslint-plugin-import";

export default [
  {
    ignores: ["build/", "dist/", "node_modules/", "craco.config.js", "tailwind.config.js", "postcss.config.js"],
  },
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      ecmaVersion: "latest",
      sourceType: "module",
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
  pluginJs.configs.recommended,
  {
    files: ["**/*.{js,jsx}"],
    plugins: {
      react: pluginReact,
      "jsx-a11y": pluginJsxA11y,
      import: pluginImport,
    },
    rules: {
      ...pluginReact.configs.recommended.rules,
      ...pluginJsxA11y.configs.recommended.rules,
      
      // React specific rules
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "warn",
      "react/jsx-uses-react": "off",
      
      // Import rules
      "import/no-unresolved": "off",
      
      // General code quality
      "no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
      "no-console": "warn",
      "prefer-const": "error",
      "no-var": "error",
      
      // Best practices
      "eqeqeq": ["error", "always"],
      "curly": ["error", "all"],
      "no-eval": "error",
      "no-implied-eval": "error",
    },
  },
];
