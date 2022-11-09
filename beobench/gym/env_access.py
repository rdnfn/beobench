"""Script to access env inside experiment container."""
import gym


def create_env():
    # Dummy method that just uses standard gym env.
    # TODO: add ability to load custom script like the env_creator script currently
    # present in beobench containers
    return gym.make("CartPole-v0")
