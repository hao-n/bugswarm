"""
Generates a Dockerfile for the job we want to reproduce, so we can spawn a container of the image built from that
Dockerfile and then run the job. gen_dockerfile.py does the following:
1. reads the .travis.yml to determine what language-named image to use
2. ADDs the script generated by travis-build into the container
3. switches to USER travis
4. runs the added script when a container is spawned.
"""
from bugswarm.common import log


def gen_dockerfile(image_tag: str, job_id: str, destination: str = None):
    """
    Generates a Dockerfile for reproducing a job.

    This only requires that we know which Travis base image from which to derive the generated Dockerfile.

    :param image_tag: The image tag that the original build used. This image tag will be used as the base image.
    :param job_id: The job ID identifying the original Travis job.
    :param destination: Path where the generated Dockerfile should be written.
    """
    log.info('Selecting Docker image to use for reproducing this job.')

    destination = destination or job_id + '-Dockerfile'
    _write_dockerfile(destination, image_tag, job_id)


def _write_dockerfile(destination: str, base_image: str, job_id: str):
    lines = [
        'FROM {}'.format(base_image),
        # Remove PPA and clean APT
        'RUN sudo rm -rf /var/lib/apt/lists/*',
        'RUN sudo rm -rf /etc/apt/sources.list.d/*',
        'RUN sudo apt-get clean',

        # Update OpenSSL and libssl to avoid using deprecated versions of TLS (TLSv1.0 and TLSv1.1).
        # TODO: Do we actually only want to do this when deriving from an image that has an out-of-date version of TLS?
        'RUN sudo apt-get update && sudo apt-get install --only-upgrade openssl libssl-dev',

        # Add the repository.
        'ADD repo-to-docker.tar /home/travis/build/',
        'RUN chmod 777 -R /home/travis/build',

        # Add the build script.
        'ADD {} /usr/local/bin/run.sh'.format(job_id + '.sh'),
        'RUN chmod +x /usr/local/bin/run.sh',

        # Set the user to use when running the image. Our Google Drive contains a file that explains why we do this.
        'USER travis',

        # Run the build script.
        'CMD ["usr/local/bin/run.sh"]',
    ]
    # Append a newline to each line and then concatenate all the lines.
    content = ''.join(map(lambda l: l + '\n', lines))
    with open(destination, 'w') as f:
        f.write(content)
