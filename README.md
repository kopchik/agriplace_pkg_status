## TODOs

[] version information is not parsed




## Assignment

```
As part of a Debian or Ubuntu operating system there is a file called status located in /var/lib/dpkg/status that holds information about software packages. 

Please write a small program using python that exposes some details about installed packages via JSON REST api.

The api should allow for the following operations:
Retrieve a list of all installed packages
View the details of an installed package: name, description, dependencies and reverse dependencies
Dependencies (other packages that the package depends on) including a reference to how to fetch the details of a dependency
Reverse dependencies (packages that have it as a dependency) including a reference to how to fetch the details of those packages
Nice to have:
Build a small FE application that allows you to visualize and navigate the packages

Considerations:
Do use python (whichever version you are comfortable with)
You may use the framework of your choice or none, the decision is yours
You may encounter alternates in the dependency list. They are presented as separated by the | (pipe) character. Try to parse and return alternates in the response.
When returning dependencies only return a reference (details link) if the dependency is included in the package file
You can find an example file here: https://gist.github.com/beetlerom/1c2d8519fd8957a123a829a1597e97de
Use this file as a source file if you do not use a Debian/Ubuntu OS.
Keep track of the time spent working on the assignment. Whatever the result, please do not spend more than 8h working on the assignment. While progress with the assignment is important there are many other factors that we will consider so don’t get stuck on trying to finish everything.
Treat this assignment as you would treat delivering production ready code




```