################### Use Mallob
FROM cvc5_base AS builder
USER root

################### Extract cvc5 in run stage
FROM satcomp-base:leader AS cvc5_liaison
WORKDIR /
# Copy mallob and solver scripts
COPY --from=builder /cvc5/build/bin/cvc5 cvc5
COPY --chown=ecs-user ./run_cvc5.sh /competition/
COPY --chown=ecs-user ./replace_solver.py /competition/
COPY --chown=ecs-user ./solver_utils.py /competition/
COPY --chown=ecs-user /solver /competition
USER ecs-user
RUN chmod +x /competition/run_cvc5.sh
RUN chmod +x /competition/solver
