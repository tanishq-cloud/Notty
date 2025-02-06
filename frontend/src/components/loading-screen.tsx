import { CSSProperties } from "react";
import PacmanLoader from "react-spinners/PacmanLoader";

const override: CSSProperties = {
  display: "block",
  margin: "0 auto",
  borderColor: "red",
};

function LoadingScreen() {
  const loading = true;
  let color = "#ffffff";

  return (
    <div className="sweet-loading">
        <div>
            Loading.......
        </div>
      <PacmanLoader
        color={color}
        loading={loading}
        cssOverride={override}
        size={150}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
    </div>
  );
}

export default LoadingScreen;