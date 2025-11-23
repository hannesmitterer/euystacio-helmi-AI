rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // ============================================================
    // HELPER FUNCTIONS
    // ============================================================
    
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isSeedbringer() {
      return isAuthenticated() && 
             request.auth.token.email == 'hannes.mitterer@gmail.com';
    }
    
    function isCouncilMember() {
      return isAuthenticated() && 
             exists(/databases/$(database)/documents/council_members/$(request.auth.uid));
    }
    
    function isOwner(memberId) {
      return isAuthenticated() && request.auth.uid == memberId;
    }
    
    function isVerifiedCouncilMember() {
      return isCouncilMember() && 
             get(/databases/$(database)/documents/council_members/$(request.auth.uid))
               .data.status == 'verified';
    }
    
    // ============================================================
    // COUNCIL MEMBERS
    // ============================================================
    
    match /council_members/{memberId} {
      // Anyone can read council member list (public governance)
      allow read: if true;
      
      // Only owner can update their own record
      allow update: if isOwner(memberId) ||
                      isSeedbringer();
      
      // Creation handled by Cloud Function only
      allow create: if false;
      
      // Deletion only by Seedbringer
      allow delete: if isSeedbringer();
    }
    
    // ============================================================
    // TESTING VOLUNTEERS
    // ============================================================
    
    match /testing_volunteers/{volunteerId} {
      // Volunteers can read their own data
      allow read: if isOwner(volunteerId) ||
                      isSeedbringer() ||
                      isVerifiedCouncilMember();
      
      // Updates only by owner or admin
      allow update: if isOwner(volunteerId) ||
                      isSeedbringer();
      
      // Creation/deletion handled by Cloud Functions
      allow create, delete: if false;
    }
    
    // ============================================================
    // SYSTEM METRICS (Public Read-Only)
    // ============================================================
    
    match /system_metrics/{document} {
      allow read: if true;
      allow write: if false; // Only Cloud Functions
    }
    
    match /system_metrics_history/{document} {
      allow read: if isAuthenticated();
      allow write: if false; // Only Cloud Functions
    }
    
    // ============================================================
    // SYSTEM LOGS (Admin Only)
    // ============================================================
    
    match /system_logs/{logId} {
      allow read: if isSeedbringer() || isVerifiedCouncilMember();
      allow write: if false; // Only Cloud Functions
    }
    
    // ============================================================
    // TESTING SESSIONS
    // ============================================================
    
    match /testing_sessions/{sessionId} {
      // Volunteers can create and read their own sessions
      allow read: if isAuthenticated() && 
                      resource.data.volunteerId == request.auth.uid;
      
      allow create: if isAuthenticated() &&
                       request.resource.data.volunteerId == request.auth.uid;
      
      // Updates only to add feedback
      allow update: if isAuthenticated() &&
                       resource.data.volunteerId == request.auth.uid;
      
      allow delete: if false;
    }
    
    // ============================================================
    // FEEDBACK
    // ============================================================
    
    match /feedback/{feedbackId} {
      // Users can read their own feedback
      allow read: if isAuthenticated() &&
                      (resource.data.submitterId == request.auth.uid ||
                       isSeedbringer());
      
      // Anyone authenticated can submit feedback
      allow create: if isAuthenticated();
      
      // No updates or deletes
      allow update, delete: if false;
    }
    
    // ============================================================
    // BUG REPORTS
    // ============================================================
    
    match /bug_reports/{bugId} {
      // Council and reporters can read
      allow read: if isAuthenticated() &&
                      (resource.data.reportedBy == request.auth.uid ||
                       isVerifiedCouncilMember() ||
                       isSeedbringer());
      
      // Authenticated users can report bugs
      allow create: if isAuthenticated();
      
      // Only council can update (for triage)
      allow update: if isVerifiedCouncilMember() || isSeedbringer();
      
      allow delete: if isSeedbringer();
    }
    
    // ============================================================
    // SIGNATURES (Council Member Submissions)
    // ============================================================
    
    match /signatures/{signatureId} {
      // Council can read all signatures
      allow read: if isCouncilMember() || isSeedbringer();
      
      // Members can submit their own signatures
      allow create: if isCouncilMember();
      
      // Only Seedbringer can verify
      allow update: if isSeedbringer();
      
      allow delete: if false;
    }
    
    // ============================================================
    // SYSTEM STATS (Public Dashboard Data)
    // ============================================================
    
    match /system_stats/{statId} {
      allow read: if true; // Public dashboard
      allow write: if false; // Only Cloud Functions
    }
  }
}
