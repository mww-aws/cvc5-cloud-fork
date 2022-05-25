################### Use Mallob
FROM cvc5_base AS builder
USER root


################### Extract cvc5 in run stage
FROM satcomp-base:leader AS cvc5_liaison
WORKDIR /
# Copy mallob and solver scripts
COPY --from=builder /mallob/build/mallob mallob
COPY --from=builder /mallob/build/mallob_sat_process mallob_sat_process
COPY --chown=ecs-user /run_mallob.sh /competition
COPY --chown=ecs-user /solver /competition
USER ecs-user
RUN chmod +x /competition/run_mallob.sh
RUN chmod +x /competition/solver
