# Project Learnings

## Performance Optimization
- Parallelizing I/O-bound tasks in Python (like network pings) using `concurrent.futures.ThreadPoolExecutor` provides significant speedup (~15x for 100 configs with 20 workers in simulated environment).
- Always verify optimizations with benchmarks and ensure functionality remains intact.
- Clean up test artifacts and temporary data files before submission.
