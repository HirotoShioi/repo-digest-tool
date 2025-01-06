import { render, RenderOptions } from "@testing-library/react";
import Providers from "@/providers";

export function customRender(ui: React.ReactNode, options?: RenderOptions) {
  return render(ui, {
    wrapper: Providers,
    ...options,
  });
}

export { customRender as render };
