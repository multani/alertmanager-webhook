# A template for Python project

## How to use?

1. Pick a project name: it should be a [valid Python module
   name](https://legacy.python.org/dev/peps/pep-0008/#package-and-module-names):

   > Modules should have short, all-lowercase names. Underscores can be used in the
   > module name if it improves readability. Python packages should also have
   > short, all-lowercase names, although the use of underscores is discouraged.

   Let's call it here: `$MY_PROJECT`.

1. Clone this repository
1. Rename the `NAME` folder to the name of your project:

   ```bash
   mv NAME $MY_PROJECT
   ```

1. Run:

   ```bash
   grep NAME -w -r . -l  | xargs sed -i "s/\<NAME\>/$MY_PROJECT/g"
   ```

1. Commit everything and start working!
