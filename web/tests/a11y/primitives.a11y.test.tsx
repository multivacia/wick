import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import {
  Alert,
  Button,
  Card,
  Inline,
  Link,
  PageHeader,
  Section,
  Skeleton,
  Stack,
  StatusBadge,
  VisuallyHidden,
} from "../../src/components/primitives";
import "../../src/styles.css";

describe("primitives accessibility smoke", () => {
  it("has no basic axe violations for a primitive composition", async () => {
    const { container } = render(
      <main>
        <PageHeader
          title="Primitives"
          description="Non-product harness"
          eyebrow="I3"
          actions={<Button>Action</Button>}
        />
        <Section title="Status">
          <Stack>
            <Inline>
              <StatusBadge status="healthy" />
              <StatusBadge status="not_ready" />
              <StatusBadge status="fault" />
            </Inline>
            <Alert tone="informational">Informational notice</Alert>
            <Card>
              <Link href="#section">Jump</Link>
              <VisuallyHidden>Hidden label</VisuallyHidden>
              <Skeleton label="Loading card" />
            </Card>
          </Stack>
        </Section>
      </main>,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
