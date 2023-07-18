FROM public.ecr.aws/sam/build-python3.9:1.90.0 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/sam/build-python3.9:1.90.0
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/
RUN pip install --upgrade pip poetry
WORKDIR /opt/work
COPY pyproject.toml /opt/work/
COPY poetry.lock /opt/work/
RUN poetry install
COPY src/ /opt/work/src/
ENV IN_CONTAINER true

CMD ["poetry", "run", "hypercorn", "src.main:app", "--bind", "0.0.0.0:8000"]
