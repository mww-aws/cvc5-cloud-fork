################### Use cvc5
FROM cvc5_base AS builder
USER root

################### Extract Mallob in run stage
FROM satcomp-base:worker AS cvc5_liaison
WORKDIR /
# Copy mallob
COPY --from=builder /mallob/build/mallob mallob
COPY --from=builder /mallob/build/mallob_sat_process mallob_sat_process
COPY --chown=ecs-user /worker /competition

RUN chmod +x /competition/worker
