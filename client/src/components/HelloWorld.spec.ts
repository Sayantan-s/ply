import { mount } from "@vue/test-utils";
import HelloWorld from "./HelloWorld.vue";

describe("HelloWorld", () => {
  it("renders props.msg when passed", () => {
    const msg = "new message";
    const wrapper = mount(HelloWorld, {
      props: { msg },
    });
    expect(wrapper.text()).toContain(msg);
  });

  it("increments count when button is clicked", async () => {
    const wrapper = mount(HelloWorld, {
      props: { msg: "test" },
    });
    const button = wrapper.find("button");
    await button.trigger("click");
    expect(button.text()).toContain("count is 1");
  });
});
