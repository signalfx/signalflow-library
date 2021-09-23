# SignalFlow Library
Modules and Examples of SignalFlow usage

# Edit and release code
1. Cut a feature branch from `master`
```bash
git checkout -b <YOUR_FEATURE_BRANCH_NAME>
```
2. Do changes and commit to your feature branch
```bash
git commit
```
3. Tag your changes with a version #
<br>
**Note:** Use [semver](https://semver.org/) versioning `<major>.<minor>.<patch>`
```bash
git tag <SEMVER_VERSION>
```
4. Push your changes to remote
```bash
git push origin <YOUR_FEATURE_BRANCH_NAME>
git push --tags
```
6. Make a release
```bash
./mkrelease <SEMVER_VERSION> 
```
**Note:** This creates `signalfx-<SEMVER_VERSION>.zip`

# Release to non-prod realms
List of non-prod realms:
- `lab0`
- `lab1`
- `rc0`
1. Upload the release zip via `<non-prod-realm>-sfc`
```bash
<non-prod-realm>-sfc sfpackage upload < signalfx-<SEMVER_VERSION>.zip
```
2. Set to current release
```bash
<non-prod-realm>-sfc sfpackage setcurrent signalfx <SEMVER_VERSION>
```

# Release to prod realms
List of prod realms can be found [here](https://signalfuse.atlassian.net/wiki/spaces/INFRA/pages/667320375/SignalFx+Realms)
1. Upload the release zip via `<prod-realm>-sfc`
```bash
<prod-realm>-sfc sfpackage upload < signalfx-<SEMVER_VERSION>.zip
```
2. Set to current release
```bash
<prod-realm>-sfc sfpackage setcurrent signalfx <SEMVER_VERSION>
```

# Rollback
```bash
<realm>-sfc sfpackage setcurrent signalfx <OLDER_STABLE_SEMVER_VERSION>
```

# How to get the current version
```bash
<realm>-sfc mb s 'sf_type:SFPackage AND sf_signalflowPackageName:signalfx' -p TSV -f sf_signalflowPackageCurrentVersion
```
