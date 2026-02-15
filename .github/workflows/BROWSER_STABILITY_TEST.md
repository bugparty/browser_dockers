# Browser Container Stability Test

This GitHub Actions workflow automatically tests the browser container's stability to ensure it doesn't crash or restart unexpectedly.

## Overview

The workflow performs a 5-minute stability test on the Chrome browser container to verify:
- The container starts successfully
- No restarts occur during the test period
- Health checks pass consistently
- The Chrome DevTools Protocol endpoint remains responsive

## When It Runs

The workflow triggers on:
- **Pull requests** that modify:
  - `Dockerfile.chrome`
  - `entrypoint.sh`
  - `compose.local.yml`
  - `.github/workflows/browser-stability-test.yml`
- **Pushes to main/master** that modify the same files
- **Manual trigger** via `workflow_dispatch`

## Test Process

### Platforms Tested
- `linux/amd64` (runs on ubuntu-latest)
- `linux/arm64` (runs on ubuntu-24.04-arm)

### Test Steps

1. **Setup**: Initializes environment and sets correct permissions for the `appuser` directory
2. **Build**: Builds the Chrome browser Docker image from `Dockerfile.chrome`
3. **Start**: Starts the browser container using docker-compose
4. **Monitor**: Performs 10 health checks over 5 minutes (every 30 seconds):
   - Verifies container is running
   - Checks restart count hasn't increased
   - Tests health endpoint (`http://127.0.0.1:9223/json/version`)
5. **Report**: Generates detailed test summary

### Success Criteria

The test passes if:
- All 10 health checks pass (100% success rate)
- Container restart count remains at 0
- Container stays in "running" state throughout
- Health endpoint responds on every check

## Test Results

Results are displayed in the GitHub Actions summary, showing:
- Platform tested (linux/amd64 or linux/arm64)
- Pass/fail status
- Total checks performed
- Number of passed/failed checks
- Detailed logs (on failure)

## Health Check Details

The health check validates:
- Container state is "running"
- Restart count hasn't increased
- Chrome DevTools Protocol endpoint at `http://127.0.0.1:9223/json/version` responds successfully

## Troubleshooting

If the test fails:
1. Check the GitHub Actions logs for detailed error messages
2. Look for "Container Logs" section to see browser output
3. Common issues:
   - Permission problems with mounted volumes
   - Resource constraints on the runner
   - Network connectivity issues
   - Chrome/Chromium startup failures

## Timeout

The entire workflow has a 15-minute timeout to prevent hanging jobs. The 5-minute test itself should complete much faster, with the additional time for build and setup.
