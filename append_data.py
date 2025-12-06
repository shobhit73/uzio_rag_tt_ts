import json
import os

target_file = 'processed_data/enriched_content.json'

new_data = [
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Weighted vs Blended Overtime – Are They the Same?",
"content": "This section clarifies the terminology around blended and weighted overtime. It explains that the term “blended overtime” is often used interchangeably with “weighted” or “weighted average overtime rate.” In all cases, the concept refers to calculating overtime based on a single averaged regular rate that accounts for multiple different hourly rates worked in the same workweek. Rather than using one job’s base rate, the system determines a combined regular rate from total straight-time earnings across all jobs and hours, and uses that blended rate to calculate overtime premiums. The section emphasizes that although different terms are used, they all describe the same fundamental compliance requirement when employees work at more than one pay rate.",
"image_descriptions": [
"A simple comparison table with two columns: one titled 'Term' listing 'Blended rate', 'Weighted overtime', 'Weighted average overtime', and the other titled 'Meaning' stating 'All refer to overtime calculated from a weighted average of multiple pay rates in a week.'"
],
"generated_questions": [
"Are blended overtime rates and weighted overtime rates different concepts or the same thing?",
"Why do people use terms like blended, weighted, or weighted-average overtime interchangeably?",
"In what situations do I need to worry about blended or weighted overtime rates instead of a single base rate?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "How to Calculate a Blended (Weighted Average) Overtime Rate",
"content": "This section walks through a step-by-step example of calculating blended overtime when an employee works two different jobs at different hourly rates in the same week. In the example, an employee named David works 30 hours as a Driver at $10/hour and 20 hours as a Cleaner at $20/hour, for a total of 50 hours, including 5 overtime hours. Step 1 is to calculate total straight-time wages by multiplying hours for each job by its rate and summing the results: (30 × $10) + (20 × $20) = $700. Step 2 is to divide the total straight-time wages by total hours worked (regular + OT + DOT) to get the blended regular rate: $700 ÷ 50 = $14/hour. Step 3 is to calculate the overtime premium: the additional half-time amount is half of the blended rate ($7). Each job’s blended overtime rate becomes its base hourly rate plus $7 (for example, Driver OT = $17/hour, Cleaner OT = $27/hour). The same idea applies for double time, using twice the blended regular rate to determine the double-time premium added to each base rate. UZIO uses this approach to properly allocate overtime and double-time wages across all jobs worked in the week.",
"image_descriptions": [
"An example calculation table with rows for 'Driver' and 'Cleaner' showing Hours (30 and 20), Rate ($10 and $20), and Straight Wages ($300 and $400) with a Total row showing 50 hours and $700 wages.",
"A small formula box showing: Step 1 – Total wages = $700; Step 2 – Blended rate = $700 ÷ 50 = $14; Step 3 – OT premium = $14 ÷ 2 = $7; Driver OT = $10 + $7 = $17; Cleaner OT = $20 + $7 = $27."
],
"generated_questions": [
"How do I compute a blended overtime rate when an employee works at two different hourly rates in the same week?",
"Why do I first calculate total straight-time wages before determining the blended regular rate?",
"In the example with David working 30 hours at $10/hour and 20 hours at $20/hour, how are the $17 and $27 overtime rates derived?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Device Requirements & Recommendations (Time Kiosk)",
"content": "This section provides guidance on choosing and configuring hardware for the UZIO Time Kiosk. It explains that the kiosk can run on tablets or computers with reliable internet access and a supported browser, and that a dedicated device per kiosk is recommended for a smoother experience. The document lists browser compatibility, typically the latest four versions of major browsers such as Chrome, Safari, Firefox, and Edge, and advises not to run the kiosk in desktop mode on Android tablets. It recommends keeping the operating system up to date so that supported browsers function properly. The section also touches on device placement and usage: each kiosk device should be dedicated to time tracking, not shared for unrelated browsing, to reduce confusion and minimize the chance of accidental closure or misconfiguration. Following these recommendations improves performance, usability, and long-term reliability of the kiosk.",
"image_descriptions": [
"A checklist-style graphic showing items like 'Tablet or PC with internet', 'Supported browser: Chrome/Safari/Firefox/Edge', 'OS up to date', and 'Dedicated device for Time Kiosk'.",
"Illustration of a tablet on a stand labeled 'Time Kiosk – Do not use for other browsing', with a small note about keeping the device plugged in and on a stable Wi-Fi network."
],
"generated_questions": [
"What kind of device and browser do I need to run the UZIO Time Kiosk reliably?",
"Why is it recommended to dedicate a specific tablet or computer solely to the Time Kiosk?",
"How do OS and browser version requirements impact the stability of the kiosk experience?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Workplace Setup: Best Practices for Kiosk Placement",
"content": "This section outlines best practices for physically placing the Time Kiosk in the workplace. It recommends choosing a convenient, easily accessible location, such as near the main entrance or a common area, so employees can quickly clock in and out without creating bottlenecks. Security is emphasized: the device should be physically secured using a stand, mounts, and locks to prevent theft or tampering. The section notes that orientation matters—if the tablet’s camera is along the shorter or longer edge, the kiosk should be used in portrait or landscape orientation accordingly so that photos and Face Unlock work correctly. Privacy is another key consideration; if Photo Security is enabled, the kiosk should not expose employees’ photos in overly public or sensitive areas. Clear, printed instructions or signage next to the device are recommended so that new employees or visitors understand exactly how to use the kiosk. Together, these practices ensure usability, security, and respect for employee privacy.",
"image_descriptions": [
"Diagram of an office floorplan with suggested kiosk locations near entrances, away from crowded hallways, and marked with icons indicating 'Easy Access' and 'Secure Mounting'.",
"Photo-style illustration of a tablet mounted on a secure stand at a doorway with a small poster next to it showing step-by-step instructions for clocking in."
],
"generated_questions": [
"Where in the workplace should I place the UZIO Time Kiosk to make clocking in and out easy for employees?",
"What physical security measures are recommended for protecting the kiosk device?",
"How should I consider camera orientation and privacy when placing a kiosk that uses Photo Security or Face Unlock?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Advanced Troubleshooting (Time Kiosk)",
"content": "This section covers advanced troubleshooting scenarios for the Time Kiosk. For PIN-related issues (such as an employee not receiving their PIN), it advises verifying that the employee’s registered email address and employment status are correct, and then resending or resetting the PIN if necessary. For Photo Security not working, it recommends checking camera permissions in the browser, testing the camera separately, and re-enabling Photo Security in kiosk settings before refreshing the page. For a kiosk that appears unresponsive, the steps include refreshing the browser tab, restarting the device, and checking for internet connectivity problems. A repeated or reappearing Activation Code can indicate that a previously activated kiosk configuration was deleted, in which case the device must be re-activated using a new Activation Code in Time Tracking Settings. These guidelines help admins quickly diagnose and correct the most common technical issues that affect kiosk usage.",
"image_descriptions": [
"Troubleshooting flow diagram starting with a problem like 'PIN Not Received' branching to checks for email correctness and a 'Resend PIN' action.",
"Screenshot sample of a browser permissions dialog showing camera access toggled on for the kiosk URL, and a small alert icon indicating connectivity or activation errors."
],
"generated_questions": [
"What steps should I take if an employee says they never received their kiosk PIN?",
"How can I fix Photo Security issues on the kiosk when the camera doesn’t seem to work?",
"What does it mean if an Activation Code keeps reappearing on a kiosk, and how do I resolve it?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Enable Time Tracking in Offline Mode",
"content": "This section explains how to enable offline mode so employees can continue tracking time even when there is no internet connection. It describes that UZIO supports a limited set of offline actions for employee time tracking through the mobile app (and optionally kiosk, if supported). To enable this capability, an employer administrator logs into the employer portal, opens Time Tracking Settings from the left navigation, navigates to the Time Clocks area, and turns on the option that allows employees to track time without an internet connection. Once enabled, supported devices can capture punches offline while the system stores the actions locally until a connection is restored and syncing can occur.",
"image_descriptions": [
"Settings screen with a toggle labeled 'Enable employees to track time without an internet connection?' under the Time Clocks section, accompanied by a short description about offline punches.",
"Small info banner explaining that offline mode is recommended for locations with unreliable network connectivity."
],
"generated_questions": [
"How do I turn on offline time tracking for employees in UZIO?",
"Which setting allows punches to be captured when there is no internet connection?",
"Why might an employer choose to enable offline mode for certain locations or devices?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "What Actions Are Allowed in Offline Mode",
"content": "This section lists what employees can and cannot do while using UZIO in offline mode. Offline capabilities are limited to core time tracking actions for employees who are already configured in Time Tracking and using the mobile app (and supported kiosk scenarios). Typically, employees can clock in, clock out, and record breaks while offline. Those actions are stored locally on the device with their timestamps and maintained in the correct sequence. More advanced actions, such as timesheet approvals, running reports, or syncing hours to payroll, are not available offline and require an active internet connection. The section clarifies that offline features are only available to employees who are active in Time Tracking and that administrative or high-impact tasks must still be performed online. This ensures that the offline mode focuses on essential punch capture while preserving data integrity and preventing complex changes without server validation.",
"image_descriptions": [
"Mobile UI mock showing a banner at the top reading 'Offline – limited features available' above buttons for Clock In, Clock Out, Break In, and Break Out.",
"A short comparison table with two columns: 'Allowed offline' listing 'Clock In, Clock Out, Take Breaks' and 'Not available offline' listing 'Timesheet Approval, Run Reports, Sync to Payroll'."
],
"generated_questions": [
"Which time tracking actions can employees perform in UZIO when their device is offline?",
"Are features like timesheet approval and payroll syncing available in offline mode?",
"Do employees need to be specially configured to use offline punches in the mobile app?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "How the System Works in Offline Mode",
"content": "This section describes the internal behavior of UZIO when an employee is working offline. While offline, the app shows a visual indicator or tag such as “Offline” so that employees know they are not connected. Any clock in/out or break actions performed in this state are recorded in secure local storage on the mobile device, with their original timestamps and in the exact sequence in which they occurred. The system maintains the order of all offline actions. Once an internet connection is restored, the app automatically begins syncing the locally stored punches to the server, typically showing a progress indicator or sync status in a corner of the app. The syncing process sends each recorded offline action to the server to be inserted into the employee’s timesheet. If there are no conflicts, the entries appear as if they had been recorded online in real time.",
"image_descriptions": [
"Mobile screen with a visible 'Offline' badge near the top and a message like 'Your punches will sync automatically when you are back online.'",
"Sync status indicator showing a small spinner or progress bar and text such as 'Syncing 3 offline punches…' once connectivity is restored."
],
"generated_questions": [
"How does UZIO store and handle time punches made while a mobile device is offline?",
"What visual cues indicate to employees that they are in offline mode and that punches will sync later?",
"What happens to offline punches when the device reconnects to the internet?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Conflict Handling in Offline Mode",
"content": "This section explains what happens when there is a conflict between offline punches and the current server state after syncing. A conflict can occur if the employee’s timesheet was changed from another device or by a manager while the mobile app was offline, or if overlapping entries are detected when offline punches are posted. When such a conflict arises, the system displays a 'Conflict Detected' prompt in the mobile app, indicating which entry is in question and showing the version that exists on the server. The employee is prompted to resolve the conflict rather than the system making an automatic decision. Two options are provided: Edit and Discard. The section emphasizes that conflict resolution is a manual step and that the employee must choose how to reconcile differences so that time records remain accurate and consistent.",
"image_descriptions": [
"Conflict dialog in the mobile app showing a message 'Conflict detected for this time entry' with a summary of the server version and the offline version and buttons for 'Edit' and 'Discard'.",
"Timeline-style view indicating where the conflicting entry sits relative to other time entries on the same day."
],
"generated_questions": [
"What is a time entry conflict in UZIO offline mode and when does it occur?",
"How does the mobile app inform employees that there is a conflict between offline and server time entries?",
"What options are available to employees when resolving offline time entry conflicts?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Edit Option for Resolving Offline Conflicts",
"content": "This section focuses on the 'Edit' option offered when resolving offline time entry conflicts. If employees choose Edit, they are taken to a screen where they can manually adjust the conflicting time entry—changing the start or end time, duration, or other relevant details—to remove overlaps or align with the current server state. Once they save the corrected entry, the app syncs the updated record back to the server, and the conflict is marked as resolved. The section notes that this process is manual and may require employees to recall their actual worked times accurately. Depending on configuration, edited entries may also be flagged for manager approval. After a successful edit and sync, the entry appears in the timesheet like any other regular time entry.",
"image_descriptions": [
"Conflict resolution screen showing editable fields for the time entry (start time, end time) with a warning banner about resolving overlaps before saving.",
"Success toast message reading 'Conflict resolved. Your time entry has been updated and synced.'"
],
"generated_questions": [
"What happens when an employee chooses the 'Edit' option for an offline time entry conflict?",
"How does editing a conflicting entry help resolve differences between offline and server data?",
"Can edited conflict entries still require manager approval after they sync?"
]
},
{
"file_name": "UZIO Time Tracking.docx",
"section_title": "Discard Option for Resolving Offline Conflicts",
"content": "This section explains the 'Discard' option during offline conflict resolution. When an employee chooses Discard, they are telling the system to ignore the conflicting offline entry and keep the server’s version (or leave no new entry if the conflict was only on the offline side). The local record of that offline punch is removed, and the conflict flag is cleared. As a result, the employee’s timesheet reflects only approved or previously synced entries, and the discarded offline entry no longer appears on the timesheet page. The section highlights that Discard should be used when the offline entry is clearly incorrect or redundant and that employees should review carefully before discarding, since this action abandons the offline changes.",
"image_descriptions": [
"Confirmation dialog with a message like 'Are you sure you want to discard this offline entry? This action cannot be undone.' and buttons 'Discard' and 'Cancel'.",
"Timesheet day view after discarding, with the previously conflicting entry removed and any conflict indicator cleared."
],
"generated_questions": [
"What does it mean to discard an offline time entry during conflict resolution in UZIO?",
"When is it appropriate for an employee to use the Discard option instead of editing the entry?",
"What happens to the timesheet and local data after an offline entry is discarded?"
]
}
]

if os.path.exists(target_file):
    with open(target_file, 'r') as f:
        existing = json.load(f)
else:
    existing = []

print(f"Original Count: {len(existing)}")
existing.extend(new_data)
print(f"New Count: {len(existing)}")

with open(target_file, 'w') as f:
    json.dump(existing, f, indent=2)

print("Data appended successfully.")
