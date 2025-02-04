import { renderRoute } from "@/test/router-test-wrapper";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import * as authService from "@/services/notes.service";
import { useNavigate } from "@tanstack/react-router";


describe("Login Page", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    localStorage.clear();
    sessionStorage.clear();
  });

  it("shows error message for invalid login", async () => {
    vi.spyOn(authService, "login").mockRejectedValue(new Error("Invalid username or password"));

    renderRoute("/login");

    await screen.findByRole("heading", { name: /sign in to your account/i });

    const usernameInput = await screen.findByPlaceholderText(/Username/i);
    const passwordInput = await screen.findByPlaceholderText(/Password/i);
    const signInButton = screen.getByRole("button", { name: /sign in/i });

    await userEvent.type(usernameInput, "wronguser");
    await userEvent.type(passwordInput, "wrongpass");
    await userEvent.click(signInButton);

    await waitFor(() => {
      expect(screen.getByText(/Invalid username or password/i)).toBeInTheDocument();
    });
  });

  it("logs in successfully and redirects to notes list", async () => {
    vi.spyOn(authService, "login").mockResolvedValue({ access_token: "mock-token", user_id: 1, full_name: "modk-name" , refresh_token: "mock-refresh" });

    renderRoute("/login");

    await screen.findByRole("heading", { name: /sign in to your account/i });

    const usernameInput = await screen.findByPlaceholderText(/Username/i);
    const passwordInput = await screen.findByPlaceholderText(/Password/i);
    const signInButton = screen.getByRole("button", { name: /sign in/i });

    await userEvent.type(usernameInput, "testuser");
    await userEvent.type(passwordInput, "password123");
    await userEvent.click(signInButton);
    expect(signInButton).toBeInTheDocument();
    screen.debug();
    await waitFor(() => {
      expect(window.location.pathname).toBe("/");
    });
  });

  it("shows validation errors when fields are empty", async () => {
    renderRoute("/login");

    await screen.findByRole("heading", { name: /sign in to your account/i });

    const signInButton = screen.getByRole("button", { name: /sign in/i });
    await userEvent.click(signInButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Username/i)).toHaveAttribute("required");
      expect(screen.getByPlaceholderText(/Password/i)).toHaveAttribute("required");
    });
  });

  it("password input should be of type password", async () => {
    renderRoute("/login");

    const passwordInput = await screen.findByPlaceholderText(/Password/i);
    expect(passwordInput).toHaveAttribute("type", "password");
  });

  vi.mock("@tanstack/react-router", async () => {
    const actual = await vi.importActual("@tanstack/react-router");
    return {
      ...actual,
      useNavigate: vi.fn(() => vi.fn()),
    };
  });

  it("clicking ‘Sign Up’ navigates to the register page", async () => {
    const mockNavigate = vi.fn();
    vi.mocked(useNavigate).mockReturnValue(mockNavigate);

  renderRoute("/login");

  const signUpButton = await screen.findByRole("button", { name: /sign up/i });
  await userEvent.click(signUpButton);

  await waitFor(() => {
    expect(mockNavigate).toHaveBeenCalledWith({ to : "/register" });
  });
});

  it("disables 'Sign in' button when loading", async () => {
    vi.spyOn(authService, "login").mockImplementation(() => new Promise(() => {}));

    renderRoute("/login");

    const usernameInput = await screen.findByPlaceholderText(/Username/i);
    const passwordInput = await screen.findByPlaceholderText(/Password/i);
    const signInButton = screen.getByRole("button", { name: /sign in/i });

    await userEvent.type(usernameInput, "testuser");
    await userEvent.type(passwordInput, "password123");
    await userEvent.click(signInButton);

    expect(signInButton).toBeDisabled();
  });
});
