# 다국어 JSON 키(Key) 생성 가이드라인 (SSOT)

> ListeningMind Hubble 로컬라이즈 키 네이밍 규칙. 이 스킬이 따르는 단일 진실 원천.

## 역할
주어진 한국어/영어 원문을 바탕으로 서비스 내 UI 구조와 의미를 가장 잘 반영하는 일관된 키를 생성한다. 다국어 지원을 위한 프론트엔드 리소스 JSON의 키를 만드는 테크니컬 라이터이자 프론트엔드 개발자의 관점으로 작업한다.

## 핵심 규칙
1. **표기법**: 모든 키는 **camelCase**. (예: `changePassword`, `agreePrivacy`)
2. **계층 구조**: 텍스트가 쓰이는 페이지/주요 컴포넌트 단위를 최상위 키(`key1`)로 그룹화한다. (예: `account`, `btn`, `dialog`, `apiLanding`, `label`, `tooltip`, `plan`, `aiOptimizer`). 세부 식별자는 `key2`.
3. **간결성(`key2` 단축 규칙)**: 영어 의미 기준으로 조사·불필요 단어를 제거하고 핵심만 담는다. 직관성을 해치지 않는 선에서 단축어(Abbreviation)를 적극 사용해 길이를 줄인다.

## 출력 규칙
1. **다국어 필수**: 결과는 항상 **한국어(ko-KR) / 일본어(ja-JP) / 영어(en-US)** 세 가지를 모두 포함한다.
2. **현행 JSON 참고**: 맥락이 헷갈리면 현행 `hubble_ko/ja/en-US.json` 을 참고해 기존 규칙과 일관성을 유지한다.
3. **CSV 기록**: 34열 시트 포맷의 행으로 산출한다. 계층은 `key1`/`key2`, 번역은 `KR`/`JP`/`US` 열에 기입한다. (→ `sheet-format.md`)
4. **중복 제외**: 요청 텍스트가 현행 JSON에 이미 존재하거나 의미·쓰임이 매우 유사한 기존 키가 있으면 **새 키를 만들지 않고 제외**한다. 이때 `삭제무방 및 비고` 열에 어떤 기존 키와 중복되어 제외했는지 **사유를 반드시 기록**한다.

## 명명 패턴
새 키는 가급적 아래 공통 패턴을 우선 따른다.

### 접미어 (Suffixes)
* **`Btn`** — 버튼 텍스트 (`loginBtn`, `saveChangeBtn`, `goToMainBtn`)
* **`Title`** — 페이지/섹션/모달 제목 (`signupCompletedTitle`, `analyzeGraphTitle`)
* **`SubTitle` / `Subcopy`** — 부제목·보조 설명 (`welcomeSubTitle`)
* **`Notice`** — 경고/주의/주요 알림 (`joinNotice`, `emailAddressNotice`)
* **`Guide` / `Desc`** — 안내 문구·폼 placeholder (`forgotPasswordGuide`)
* **`Label`** — 폼 요소/필드 이름, 짧은 식별명 (`rootDomainLabel`)

### 접두어 (Prefixes)
* **`helptext`** — 폼 입력창 하단 도움말, 유효성 에러/성공 메시지 (`helptextEmailAuthCodeCheck`, `helptextEmailAuthSend`)
* **`goTo`** — 페이지/외부 링크 이동 액션 (`goToBlog`, `goToInstallGuide`)
* **동사 원형** — 명확한 동작이면 동사로 시작 (`add`, `delete`, `edit`, `save`, `cancel`)

### 형제 기능 미러링 (중요)
새 기능 키는 기능적으로 대응하는 **기존 형제 기능의 구조를 그대로 미러링**한다.
- 예) `plan.tablecepFinder*` → `plan.tableaiOptimizer*` (플랜 비교표 행 구조 동일 복제)
- 예) `tooltip.tablecepFinder1` → `tooltip.tableaiOptimizer1` ('검색' → '분석' 어휘만 치환)
- 공용 라벨(X축/Y축처럼 여러 화면에서 재사용 가능한 것)은 전용 기능 네임스페이스가 아니라 공용 `label` 네임스페이스에 둔다.

## 예시 (Few-Shot)
- "비밀번호 재설정" / 버튼 → `changePasswordBtn` (상위가 뚜렷하면 `btn` > `changePassword`)
- "원활한 서비스를 위해 정확한 정보를 입력해주세요." / 안내(경고), `signupForm` → `signupFormNotice`
- "가입한 이메일 주소를 입력해주세요." / placeholder, `forgotPassword` → `forgotPasswordGuide`
- "인증코드가 맞지 않습니다. 다시 확인해주세요." / 에러, 이메일 인증 → `helptextEmailAuthCodeCheck`

## 입력 포맷
새 문자열마다 다음 메타데이터를 받아 가장 적합한 계층 키를 설계한다:
- 한국어 원문
- 컴포넌트 유형 (버튼/타이틀/안내문/라벨/툴팁 등)
- 소속 화면/카테고리
