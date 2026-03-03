export interface IJDInputForm {
  jd: string;
  file: File | null;
  cvLink: string;
}

export interface IJDMatchStatusResponse {
  fileId: string;
}

export interface DataHandlers {
  handleSubmit: () => Promise<void>;
  handleReset: (eve: Event) => void;
  handleChange: (file: File | null) => Promise<void>;
  handleChangeTabs: (value: ETAB) => void;
}

export interface DataSource {
  loading: globalThis.Ref<boolean, boolean>;
  jdMatchInfo: globalThis.Ref<globalThis.JDMatchInfoResponse, globalThis.JDMatchInfoResponse>;
  form: globalThis.Ref<IJDInputForm, IJDInputForm>;
  fileId: globalThis.Ref<string | null, string | null>;
  tab: globalThis.Ref<ETAB, ETAB>;
  status: globalThis.Ref<globalThis.JDMATCH_STATUS, globalThis.JDMATCH_STATUS>;
  resumeLink: globalThis.Ref<string, string>;
}

export const dataHandlerInjectionKey: InjectionKey<DataHandlers> = Symbol("data-handlers");

export const dataSourceInjectionKey: InjectionKey<DataSource> = Symbol("data-source");

export enum ETAB {
  TAB_1 = "tab-input",
  TAB_2 = "tab-result",
}
