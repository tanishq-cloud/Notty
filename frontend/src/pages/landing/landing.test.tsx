import { screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { renderRoute } from "@/test/router-test-wrapper";
import * as authHook from "@/hooks/use-auth";

describe("Landing Page", () => {
  it("renders the Landing Page component", async () => {
    renderRoute("/");
    
    //Checkin if the document is not blank and text is present
    expect(await screen.findByRole('heading', { name: /Capture Your Thoughts with Notty/i })).toBeInTheDocument();
    expect(screen.getByText(/A simple and powerful note-taking app with a rich text editor. Stay organized and never forget an idea again./i)).toBeInTheDocument();
    
    // Check for the Login button
    const getStartedButton = screen.getByRole('button', { name: /Login/i });
    const loginButton = screen.getByRole('button', {name: /Get Started/i})

    expect(getStartedButton).toBeInTheDocument();
    expect(loginButton).toBeInTheDocument(); //It means person is not authenticated
  });

  // Test for authenticated users
  it("navigates to the list page for authenticated users", async () => {
    // Mock useAuth to return true
    vi.spyOn(authHook, "useAuth").mockReturnValue(true);

    renderRoute("/");
    console.log(document.body.innerHTML)
    expect(screen.getByRole('button', { name: /Create New Note/i })); //checking authenticated person can see
})});
