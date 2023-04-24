/** @type {import('tailwindcss').Config} */

const Path = require("path");
const pwd = process.env.PWD;

// We can add 3-party python packages here
const pySitePackages = "../venv/lib/python3.10/site-packages";

// We can add current project paths here
const projectPaths = [
    Path.join(pwd, "../templates/**/*.{html,js}"),
    Path.join(pwd, "../static/**/*.{html,js}"),
    // add js file paths if you need
];

// We can add 3-party python packages here
let pyPackagesPaths = []
if (pySitePackages) {
    pyPackagesPaths = [
        Path.join(pySitePackages, "./crispy_tailwind/**/*.html"),
        Path.join(pySitePackages, "./crispy_tailwind/**/*.py"),
        Path.join(pySitePackages, "./crispy_tailwind/**/*.js"),
    ];
}

const contentPaths = [...projectPaths, ...pyPackagesPaths];
console.log(`tailwindcss will scan ${contentPaths}`);

module.exports = {
    content: contentPaths,
    theme: {
        extend: {
            fontFamily: {
                'lato': ['Lato', 'sans-serif']
            }
        },
    },
    plugins: [
        // require('@tailwindcss/forms'),
    ],
    mode: "aot",
}

