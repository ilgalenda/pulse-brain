"""embedding — the provider-agnostic embedding interface (MODEL-RETRIEVAL.md §3.1).

ONE JOB: turn page text into a vector, behind a swappable adapter, so the model stays
pluggable (the kernel's `model-route` for the `embedding` role). Three adapters share one
interface:

  - StubEmbedder  — deterministic, dependency-free; used cold and in tests. Same text →
                    same vector, always. This is what makes the substrate SHELL runnable
                    and fixture-testable without a model pull.
  - LocalAdapter  — on-device model (zero-API-config). The model is FETCHED UNTRUSTED
                    INPUT: pinned id + checksum, verified on pull, fail-closed
                    (PRINCIPLES.md §3). The pull itself is S19-deferred — the interface
                    and the pin mechanism ship now; embed() raises NotConfigured until a
                    verified model is present.
  - ApiAdapter    — opt-in upgrade. Key strictly via .env; activates only when the key is
                    present. The network call is S19-deferred (NotConfigured).

BOUNDS: the StubEmbedder is deterministic and dependency-free. The real adapters MAY use
the network and (Api) a credential — which is why this is engine `substrate`, not a
Builder `tool` (BUILDER.md §3). No adapter writes anything; embedding text is data.
"""

import hashlib
import math
import os


class NotConfigured(RuntimeError):
    """A real adapter was asked to embed before its S19 setup (model pull / API key)."""


class ChecksumMismatch(RuntimeError):
    """A fetched model's checksum did not match the pinned value — fail closed."""


def _normalise(vector):
    """Unit-normalise so cosine similarity is a plain dot product. Zero stays zero."""
    norm = math.sqrt(sum(component * component for component in vector))
    if norm == 0.0:
        return list(vector)
    return [component / norm for component in vector]


def verify_checksum(path, expected_sha256):
    """Verify a fetched model file against its pinned checksum, or raise (fail closed).

    The local model is untrusted fetched input; a mismatch means a tampered or wrong
    artifact and MUST stop the run rather than embed with it (MODEL-RETRIEVAL.md §3.6).
    """
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual != expected_sha256:
        raise ChecksumMismatch(
            f"model checksum mismatch for {path}: expected {expected_sha256}, got {actual}"
        )


class EmbeddingAdapter:
    """The interface every adapter honours. `dim` is fixed per adapter; `embed` is pure
    of any store state (it only maps text → vector)."""

    name = "abstract"
    dim = 0

    def embed(self, text):
        raise NotImplementedError

    def embed_batch(self, texts):
        return [self.embed(text) for text in texts]


class StubEmbedder(EmbeddingAdapter):
    """Deterministic, dependency-free embedder for cold runs and fixture tests.

    Derives `dim` floats in [-1, 1] from the SHA-256 of the text, then unit-normalises.
    It is NOT semantically meaningful — it exists so the store / staleness / re-rank /
    dedup machinery (the deterministic shell) can be exercised end-to-end without a real
    model. The real adapters below are what carry meaning at S19.
    """

    name = "stub"

    def __init__(self, dim=64):
        self.dim = dim

    def embed(self, text):
        components = []
        counter = 0
        # Stretch the hash to `dim` floats by hashing (text, counter) blocks; each byte
        # pair → one float in [-1, 1]. Deterministic for a given (text, dim).
        while len(components) < self.dim:
            block = hashlib.sha256(f"{counter}\x00{text}".encode("utf-8")).digest()
            for i in range(0, len(block) - 1, 2):
                if len(components) >= self.dim:
                    break
                value = (block[i] << 8) | block[i + 1]
                components.append((value / 32767.5) - 1.0)
            counter += 1
        return _normalise(components)


class LocalAdapter(EmbeddingAdapter):
    """On-device embedding model — the zero-API-config default. Ships the interface + the
    pin/verify mechanism now; the model pull and the actual encode are S19-deferred.

    `model_id` and `expected_sha256` are pinned (placeholders in the engine, real values
    at S19). `load()` verifies a present model file's checksum (fail closed); `embed`
    raises NotConfigured until a verified model is loaded.
    """

    name = "local"

    def __init__(self, model_id, expected_sha256, model_path=None, dim=0):
        self.model_id = model_id
        self.expected_sha256 = expected_sha256
        self.model_path = model_path
        self.dim = dim
        self._model = None

    def load(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            raise NotConfigured(
                f"local model '{self.model_id}' is not present — pull + pin it at S19 "
                "(MODEL-RETRIEVAL.md §3.6); the engine ships the interface, not the model"
            )
        verify_checksum(self.model_path, self.expected_sha256)
        # The actual model load (e.g. a sentence-transformer) is wired at S19, against the
        # dependency declared in requirements.txt. Until then, loading a verified file is
        # as far as the shell goes.
        raise NotConfigured(
            "local model encode is wired at S19; the checksum-verified pull is in place"
        )

    def embed(self, text):
        if self._model is None:
            self.load()
        raise NotConfigured("local model encode is wired at S19")


class ApiAdapter(EmbeddingAdapter):
    """Opt-in API embeddings. Activates ONLY when the key env var is set; the provider
    call is S19-deferred. Documents the data-boundary cost: canon text leaves the device
    (MODEL-RETRIEVAL.md §3.1/§5)."""

    name = "api"

    def __init__(self, key_env_var, model_id, dim=0):
        self.key_env_var = key_env_var
        self.model_id = model_id
        self.dim = dim

    def _require_key(self):
        key = os.environ.get(self.key_env_var)
        if not key:
            raise NotConfigured(
                f"API embeddings need {self.key_env_var} in the environment (.env) — "
                "absent, so this adapter is inactive; the local adapter is the default"
            )
        return key

    def embed(self, text):
        self._require_key()
        raise NotConfigured("API embedding provider call is wired at S19")
