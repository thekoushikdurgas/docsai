"use client";

import { useState } from "react";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@/components/ui/Tabs";
import { Progress } from "@/components/ui/Progress";
import { Checkbox } from "@/components/ui/Checkbox";
import { Radio, RadioGroup } from "@/components/ui/Radio";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import {
  ContextMenu,
  ContextMenuTrigger,
  ContextMenuContent,
  ContextMenuItem,
} from "@/components/ui/ContextMenu";

export default function UiKitPage() {
  const [checked, setChecked] = useState(false);
  const [radio, setRadio] = useState("a");

  return (
    <AdminPageLayout title="UI kit" subtitle="Admin design system primitives">
      <Tabs defaultValue="controls" variant="underline">
        <TabsList>
          <TabsTrigger value="controls">Controls</TabsTrigger>
          <TabsTrigger value="feedback">Feedback</TabsTrigger>
        </TabsList>
        <TabsContent value="controls">
          <div className="c360-flex c360-flex--col c360-flex--gap-4" style={{ maxWidth: 480 }}>
            <Button>Primary</Button>
            <Button variant="outline">Outline</Button>
            <Input label="Sample input" placeholder="Type here" />
            <Checkbox
              label="Checkbox"
              checked={checked}
              onChange={setChecked}
            />
            <RadioGroup name="demo" value={radio} onChange={setRadio}>
              <Radio value="a" label="Option A" />
              <Radio value="b" label="Option B" />
            </RadioGroup>
            <Badge color="primary">Badge</Badge>
          </div>
        </TabsContent>
        <TabsContent value="feedback">
          <Progress value={65} />
          <ContextMenu>
            <ContextMenuTrigger asChild>
              <div
                className="c360-card"
                style={{ padding: 24, marginTop: 16, cursor: "context-menu" }}
              >
                Right-click for context menu
              </div>
            </ContextMenuTrigger>
            <ContextMenuContent>
              <ContextMenuItem>Action one</ContextMenuItem>
              <ContextMenuItem>Action two</ContextMenuItem>
            </ContextMenuContent>
          </ContextMenu>
        </TabsContent>
      </Tabs>
    </AdminPageLayout>
  );
}
