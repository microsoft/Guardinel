# Guardinel

# Introduction
Guardinel is a policy compliance tool that can be used to enforce rules on the PR.

When you want to run some validations on the PRs raised for a branch in your repository, you can write them as Guardinel policies and deploy them as one of the branch policies.

Policies could be anything:
- You might wanna block users from editing a particular file or files in a path
- You want to check if automation is added to the PR
- You might want to check some service for any violation before merging the PR
- You might wanna get the PR approved frmo specific person since it modifies a certain file

Policies vary according to the teams, products and their business. Only your imagination is the limit to build the policy. 
Guardinel provides a base framework that can help you regulate your business standards on the PRs.

# How to run
## Tools
 1. [PyCharm](https://www.jetbrains.com/pycharm/download/#section=mac) by Intellij
 2. Python
 3. Install python package - response 

## Generate PAT
Generate PAT following instructions mentioned [here](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page))

## Code set-up

- Clone this repository
- Inside PyCharm, open project release-velocity. From PyCharm -> Preferences menu, navigate to Project Structure and mark **compliance** folder as Source.

## Execution 

### Pycharm
- On PyCharm navigate to automation -> compliance -> policy_checker.py
- Then right-click and Run 'policy_checker' or Click on the green button next to the main in the policy_checker.py
- you will be able to see a policy_checker configuration, click on it and then Edit Configurations.    
- inside Edit Configurations dialog, set the parameters to the following:
``` 
-p policy_name -d <YOUR_DOMOREXP_PAT> -i <PR_NUM> -t android/ios
```

### Command line
You can invoke the script in the format below:
```
python3 ./release-velocity/automation/compliance/policy_checker.py -p policy_name -d <YOUR_DOMOREXP_PAT> -i <PR_NUM> -t android/ios
```

## Execution flow
1. SHIELD is invoked using a driver script (policy_checker.py) to which we will be passing a set of policies/actions to execute. Driver script will build a config object using the cmdline params
2. ConcurrentExecutor will evaluate all the overrides attached to the policies/actions and retains the value until the shield execution is completed
3. ConcurrentExecutor will execute the Policy/Action in threads. Each thread will 
     - check if any of the overrides is evaluated to true. If Yes, return resuls as OVERRIDEN
     - invoke the execute method of the policy/action, if it is not evaluated to OVERRIDEN
4. invoke the callback_actions configured for the task. Callback actions are more like a finally method for try-catch block. It always gets executed.
5. & 6. Once all the threads have returns with their results, configured notifiers and telemetries are invoked.
7. Once the result is received back at driver script, the script checks if there are any failed policies. If yes, it exits with 1 which will fails the gate. If not, exits with code 0 which passes the gate.

# Basic components
SHIELD comprises the following basic components
- Task
    - Abstract class that defines the skeleton of the policies
    - Implementations should override execute() method to validate the PR for a specific condition. Ex: Bug jail policy validates if the team who raised the PR is in bug jail or not.
- Action
    - Abstract sub-class of Task that defines the actions taken by the shield
    - Proactive changes that could reduce the opex work will be its implementation. Ex: Attach ECS work item to the PR, Clone the bug to the next release train
    - Actions will always return either NO_ACTION or NOTIFY.
    - Actions can be made a callback action for a task by adding its identifier in the task's actions() method
- Override
    - Abstract class that defines an override for a task/action 
    - Override are specific conditions on which shield will make an exception on certain policies
    - Overrides are configured within the policies. If an override is configured in the shield cmdline param, it will be considered as a global override which can override all the policies if evaluated to true
- Notifier
    - Abstract class that defines a notifier
    - The notifiers are invoked after all the policies have completed their execution
- Telemetry
    - Abstract class that defines a metrics class
    - Ideally, the metrics are collected by default on all the policies
    - Implementation will have make use of the MetricsData object to get the info that they want to log
- Template
    - Templates are abstract classes that abstract the redundant code into a unit which can be reused by multiple components
    - Ex: If we need to restrict users from modifying specific files, we need to check if the file has been modified in the PR. If for different repo, different files are to be restricted, we can extract the logic to fetch the modified files from the PR and reuse it while validating for the files in question. 
